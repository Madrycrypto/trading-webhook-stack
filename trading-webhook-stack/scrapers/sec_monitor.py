#!/usr/bin/env python3
"""
SEC Form 4 Insider Trading Monitor
Integrates with your existing trading webhook stack

Usage:
    python scrapers/sec_monitor.py --ticker AAPL --interval 30
    python scrapers/sec_monitor.py --watchlist tickers.txt
"""

import argparse
import asyncio
import aiohttp
import feedparser
import sqlite3
import logging
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Webhook configuration
WEBHOOK_URL = "http://localhost:3000/webhook/insider-trading"

class SECForm4Monitor:
    """Monitor SEC Form 4 filings with webhook integration"""

    def __init__(
        self,
        db_path: str = 'insider_trading.db',
        webhook_url: str = WEBHOOK_URL
    ):
        self.db_path = db_path
        self.webhook_url = webhook_url
        self.seen_entries: Set[str] = set()
        self.init_database()
        self.load_seen_entries()

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main filings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS filings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                accession_number TEXT UNIQUE NOT NULL,
                ticker TEXT,
                company_name TEXT,
                cik TEXT,
                filing_date TEXT,
                filed_date TEXT,
                notified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_data TEXT
            )
        ''')

        # Insiders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insiders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cik TEXT,
                name TEXT,
                title TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(cik, name)
            )
        ''')

        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filing_id INTEGER REFERENCES filings(id),
                insider_id INTEGER REFERENCES insiders(id),
                transaction_type TEXT,
                shares INTEGER,
                price REAL,
                total_value REAL,
                shares_owned_after INTEGER,
                transaction_date TEXT,
                UNIQUE(filing_id, insider_id, transaction_date, shares)
            )
        ''')

        # Seen entries tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seen_entries (
                entry_id TEXT PRIMARY KEY,
                seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def load_seen_entries(self):
        """Load previously seen entry IDs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT entry_id FROM seen_entries')
        self.seen_entries = {row[0] for row in cursor.fetchall()}
        conn.close()
        logger.info(f"Loaded {len(self.seen_entries)} seen entries")

    def is_seen(self, entry_id: str) -> bool:
        """Check if entry was already seen"""
        return entry_id in self.seen_entries

    def mark_seen(self, entry_id: str):
        """Mark entry as seen"""
        if entry_id not in self.seen_entries:
            self.seen_entries.add(entry_id)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO seen_entries (entry_id) VALUES (?)', (entry_id,))
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # Already exists
            finally:
                conn.close()

    async def fetch_sec_rss(self, tickers: Optional[List[str]] = None) -> List[Dict]:
        """Fetch SEC RSS feed for Form 4 filings"""

        # Build URL
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar"

        if tickers:
            # Fetch individual tickers
            feeds = []
            for ticker in tickers[:10]:  # Limit to 10 concurrent requests
                url = f"{base_url}?action=getcompany&CIK={ticker}&type=4&count=10&owner=only&output=atom"
                feeds.append(url)
        else:
            # Fetch all recent filings
            url = f"{base_url}?action=getcurrent&type=4&count=100&owner=only&output=atom"
            feeds = [url]

        # Fetch all feeds
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_feed(session, url) for url in feeds]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine results
        all_entries = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error fetching feed: {result}")
                continue
            all_entries.extend(result)

        logger.info(f"Fetched {len(all_entries)} total entries")
        return all_entries

    async def fetch_feed(self, session: aiohttp.ClientSession, url: str) -> List[Dict]:
        """Fetch single RSS feed"""
        try:
            headers = {
                'User-Agent': 'InsiderTradingMonitor/1.0 (contact: your-email@example.com)'
            }

            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 200:
                    logger.error(f"HTTP {response.status} for {url}")
                    return []

                content = await response.text()

            # Parse RSS
            feed = feedparser.parse(content)
            entries = []

            for entry in feed.entries:
                # Extract accession number from link
                link = entry.get('link', '')
                accession = link.split('accession_number=')[-1].split('&')[0] if 'accession_number=' in link else ''

                # Get company info
                summary = entry.get('summary', '')
                company_name = entry.get('sec_company_name', '')

                entries.append({
                    'accession_number': accession,
                    'ticker': self.extract_ticker(summary),
                    'company_name': company_name,
                    'cik': entry.get('sec_cik', ''),
                    'filing_date': entry.get('filing_date', {}).get('day', ''),
                    'filed_date': entry.get('date', ''),
                    'url': link,
                    'summary': summary
                })

            return entries

        except Exception as e:
            logger.error(f"Error parsing feed from {url}: {e}")
            return []

    def extract_ticker(self, summary: str) -> str:
        """Extract ticker from summary text"""
        # Simple extraction - looks for ticker pattern
        import re
        match = re.search(r'Ticker:\s*([A-Z]{1,5})', summary)
        return match.group(1) if match else ''

    async def send_to_webhook(self, data: Dict):
        """Send filing data to webhook"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        logger.info(f"Sent webhook for {data.get('ticker')}: {data.get('company')}")
                    else:
                        logger.error(f"Webhook failed: HTTP {response.status}")

        except Exception as e:
            logger.error(f"Error sending webhook: {e}")

    async def process_entries(self, entries: List[Dict], notify: bool = True):
        """Process filing entries"""
        new_filings = 0

        for entry in entries:
            entry_id = entry['accession_number']

            if not entry_id:
                continue

            # Skip if already seen
            if self.is_seen(entry_id):
                continue

            # Mark as seen
            self.mark_seen(entry_id)

            # Save to database
            self.save_filing(entry)

            # Send webhook notification
            if notify:
                webhook_data = {
                    'type': 'insider_trading',
                    'ticker': entry['ticker'],
                    'company': entry['company_name'],
                    'filing_date': entry['filing_date'],
                    'url': entry['url'],
                    'timestamp': datetime.now().isoformat()
                }

                await self.send_to_webhook(webhook_data)

            new_filings += 1

        logger.info(f"Processed {new_filings} new filings")
        return new_filings

    def save_filing(self, entry: Dict):
        """Save filing to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR IGNORE INTO filings
                (accession_number, ticker, company_name, cik, filing_date, filed_date, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry['accession_number'],
                entry['ticker'],
                entry['company_name'],
                entry['cik'],
                entry['filing_date'],
                entry['filed_date'],
                json.dumps(entry)
            ))

            conn.commit()

        except Exception as e:
            logger.error(f"Error saving filing: {e}")
        finally:
            conn.close()

    async def monitor(self, tickers: Optional[List[str]] = None, interval_minutes: int = 30):
        """Continuous monitoring loop"""
        logger.info(f"Starting monitoring (interval: {interval_minutes}min)")

        if tickers:
            logger.info(f"Watching tickers: {', '.join(tickers)}")

        while True:
            try:
                # Fetch new entries
                entries = await self.fetch_sec_rss(tickers)

                # Process entries
                await self.process_entries(entries, notify=True)

                # Wait for next interval
                logger.info(f"Waiting {interval_minutes} minutes until next check...")
                await asyncio.sleep(interval_minutes * 60)

            except KeyboardInterrupt:
                logger.info("Stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)

    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Total filings
        cursor.execute('SELECT COUNT(*) FROM filings')
        stats['total_filings'] = cursor.fetchone()[0]

        # Filings in last 24h
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM filings WHERE created_at > ?', (yesterday,))
        stats['last_24h'] = cursor.fetchone()[0]

        # Top tickers
        cursor.execute('''
            SELECT ticker, COUNT(*) as count
            FROM filings
            WHERE ticker IS NOT NULL AND ticker != ''
            GROUP BY ticker
            ORDER BY count DESC
            LIMIT 10
        ''')
        stats['top_tickers'] = dict(cursor.fetchall())

        conn.close()
        return stats


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='SEC Form 4 Insider Trading Monitor')
    parser.add_argument('--ticker', action='append', help='Ticker(s) to monitor')
    parser.add_argument('--watchlist', type=str, help='File with ticker list (one per line)')
    parser.add_argument('--interval', type=int, default=30, help='Check interval in minutes')
    parser.add_argument('--webhook', type=str, default=WEBHOOK_URL, help='Webhook URL')
    parser.add_argument('--db', type=str, default='insider_trading.db', help='Database path')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--stats', action='store_true', help='Show statistics and exit')

    args = parser.parse_args()

    # Load watchlist
    tickers = args.ticker or []

    if args.watchlist:
        watchlist_path = Path(args.watchlist)
        if watchlist_path.exists():
            with open(watchlist_path) as f:
                tickers.extend([line.strip() for line in f if line.strip()])
        else:
            logger.error(f"Watchlist file not found: {args.watchlist}")
            sys.exit(1)

    # Create monitor
    monitor = SECForm4Monitor(db_path=args.db, webhook_url=args.webhook)

    # Show stats
    if args.stats:
        stats = monitor.get_stats()
        print("\n=== SEC Form 4 Monitor Statistics ===")
        print(f"Total filings: {stats['total_filings']}")
        print(f"Last 24 hours: {stats['last_24h']}")
        print("\nTop tickers:")
        for ticker, count in stats['top_tickers'].items():
            print(f"  {ticker}: {count}")
        sys.exit(0)

    # Run once
    if args.once:
        logger.info("Running single check...")
        entries = await monitor.fetch_sec_rss(tickers if tickers else None)
        await monitor.process_entries(entries, notify=True)
        logger.info("Done!")
        sys.exit(0)

    # Continuous monitoring
    await monitor.monitor(tickers if tickers else None, interval_minutes=args.interval)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
        sys.exit(0)
