#!/usr/bin/env python3
"""
Insider Trading Monitor - Simplified Working Version
Uses SEC data API (no XML parsing needed)
"""

import requests
import json
import sqlite3
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Configuration
WEBHOOK_URL = "http://localhost:3000/webhook/insider-trading"
SEC_BASE_URL = "https://www.sec.gov"

class InsiderMonitor:
    """Simplified SEC Form 4 monitor"""

    def __init__(self, db_path='insider_monitor.db'):
        self.db_path = db_path
        self.ticker_to_cik = {}
        self.init_database()
        self.load_tickers()

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main filings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS filings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                cik TEXT,
                accession_number TEXT,
                filing_date TEXT,
                form TEXT,
                notified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(ticker, accession_number)
            )
        ''')

        # Watchlist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT UNIQUE,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Database initialized")

    def load_tickers(self):
        """Load ticker to CIK mappings from SEC"""
        url = f"{SEC_BASE_URL}/files/company_tickers.json"

        try:
            response = requests.get(url, headers={
                'User-Agent': 'Insider Monitor (test@example.com)',
                'Accept': 'application/json'
            })
            response.raise_for_status()
            data = response.json()

            for item in data.values():
                ticker = item['ticker'].upper()
                cik = str(item['cik_str']).zfill(10)
                self.ticker_to_cik[ticker] = cik

            print(f"✅ Loaded {len(self.ticker_to_cik)} ticker mappings")
        except Exception as e:
            print(f"❌ Error loading tickers: {e}")

    def get_cik(self, ticker: str) -> Optional[str]:
        """Get CIK for ticker"""
        return self.ticker_to_cik.get(ticker.upper())

    def get_form4_filings(self, ticker: str, days_back: int = 7) -> List[Dict]:
        """Get recent Form 4 filings"""
        cik = self.get_cik(ticker)
        if not cik:
            print(f"❌ Ticker {ticker} not found")
            return []

        # Use SEC data API (more reliable)
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        try:
            response = requests.get(url, headers={
                'User-Agent': 'Insider Monitor (test@example.com)',
                'Accept': 'application/json'
            })
            response.raise_for_status()
            data = response.json()

            filings = data['filings']['recent']
            cutoff_date = datetime.now() - timedelta(days=days_back)

            form4_filings = []
            for i in range(len(filings['form'])):
                if filings['form'][i] == '4':
                    filing_date = datetime.strptime(filings['filingDate'][i], '%Y-%m-%d')
                    if filing_date >= cutoff_date:
                        form4_filings.append({
                            'ticker': ticker,
                            'cik': cik,
                            'accession_number': filings['accessionNumber'][i],
                            'filing_date': filings['filingDate'][i]
                        })

            return form4_filings

        except Exception as e:
            print(f"❌ Error fetching filings: {e}")
            return []

    def save_filings(self, ticker: str, filings: List[Dict]):
        """Save filings to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        new_count = 0
        for filing in filings:
            try:
                cursor.execute('''
                    INSERT INTO filings (ticker, cik, accession_number, filing_date, form)
                    VALUES (?, ?, ?, ?, ?)
                ''', (ticker, filing['cik'], filing['accession_number'], filing['filing_date'], '4'))
                new_count += 1
            except sqlite3.IntegrityError:
                pass  # Already exists

        conn.commit()
        conn.close()
        return new_count

    def send_webhook(self, ticker: str, filing_count: int, latest_date: str):
        """Send alert to webhook"""
        payload = {
            'type': 'insider_trading',
            'ticker': ticker,
            'company': ticker,
            'filing_count': filing_count,
            'latest_filing': latest_date
        }

        try:
            response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Webhook sent for {ticker}")
                return True
        except Exception as e:
            print(f"⚠️  Webhook error: {e}")

        return False

    def monitor_ticker(self, ticker: str, days_back: int = 7):
        """Monitor a single ticker"""
        print(f"\n📊 Monitoring {ticker}...")

        filings = self.get_form4_filings(ticker, days_back)

        if filings:
            new_filings = self.save_filings(ticker, filings)

            if new_filings > 0:
                latest = filings[0]['filing_date']
                print(f"   📋 Found {len(filings)} filings ({new_filings} new)")
                print(f"   📅 Latest: {latest}")

                # Send webhook
                self.send_webhook(ticker, len(filings), latest)
            else:
                print(f"   ℹ️  {len(filings)} filings (no new)")
        else:
            print(f"   ℹ️  No Form 4 filings found")

    def add_to_watchlist(self, ticker: str):
        """Add ticker to watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO watchlist (ticker) VALUES (?)', (ticker.upper(),))
            conn.commit()
            print(f"✅ Added {ticker} to watchlist")
        except sqlite3.IntegrityError:
            print(f"ℹ️  {ticker} already in watchlist")

        conn.close()

    def run_watchlist(self, days_back: int = 7):
        """Monitor all tickers in watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT ticker FROM watchlist WHERE active = 1')
        tickers = [row[0] for row in cursor.fetchall()]
        conn.close()

        print(f"\n🔍 Monitoring {len(tickers)} tickers in watchlist...")

        for ticker in tickers:
            self.monitor_ticker(ticker, days_back)


def main():
    parser = argparse.ArgumentParser(description='Insider Trading Monitor')
    parser.add_argument('--ticker', help='Monitor specific ticker')
    parser.add_argument('--tickers', help='Monitor multiple tickers (comma-separated)')
    parser.add_argument('--add', help='Add ticker to watchlist')
    parser.add_argument('--watchlist', action='store_true', help='Run watchlist monitoring')
    parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

    args = parser.parse_args()

    monitor = InsiderMonitor()

    if args.ticker:
        monitor.monitor_ticker(args.ticker, args.days)
    elif args.tickers:
        for ticker in args.tickers.split(','):
            monitor.monitor_ticker(ticker.strip(), args.days)
    elif args.add:
        monitor.add_to_watchlist(args.add)
    elif args.watchlist:
        monitor.run_watchlist(args.days)
    else:
        # Default: monitor popular tech stocks
        print("\n📊 Monitoring popular tech stocks...")
        tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
        for ticker in tech_stocks:
            monitor.monitor_ticker(ticker, args.days)


if __name__ == '__main__':
    main()
