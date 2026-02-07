# Web Scraping & Monitoring for Financial Data - Summary

## Overview

This guide provides a complete, production-ready implementation for scraping and monitoring insider trading disclosures from SEC Form 4 filings. The solution integrates seamlessly with your existing trading webhook stack.

## What You've Learned

### 1. Web Scraping Techniques

**Tools Comparison:**

| Tool | Best For | Language | Speed | Difficulty |
|------|----------|----------|-------|------------|
| **BeautifulSoup** | Static HTML | Python | Medium | Easy |
| **requests + lxml** | Fast static scraping | Python | Very Fast | Easy |
| **Playwright** | Dynamic JS content | Python/Node | Fast | Medium |
| **Puppeteer** | Chrome automation | Node.js | Fast | Medium |
| **Scrapy** | Large-scale scraping | Python | Very Fast | Medium |

**Key Takeaways:**
- Use RSS feeds when available (SEC provides them!)
- Use BeautifulSoup for simple static sites
- Use Playwright/Puppeteer for dynamic JavaScript content
- Always implement rate limiting
- Cache results to reduce server load

### 2. Change Detection

**Three Approaches:**

1. **RSS Feeds (Recommended)**
   - SEC provides official RSS feeds for Form 4
   - No scraping needed - parse XML
   - Real-time updates
   - Respectful and legal

2. **Hash Comparison**
   - Store hash of page content
   - Compare on each check
   - Good for static pages

3. **Database Tracking**
   - Store seen entry IDs
   - Check database before processing
   - Prevents duplicates

### 3. Monitoring Strategies

**Polling vs. Push-Based:**

**Polling (Recommended for RSS):**
```python
# Check every 30 minutes
python sec_monitor.py --interval 30
```
- Simple implementation
- Works everywhere
- Control over frequency
- Can miss rapid updates

**Push-Based (Webhooks):**
- Instant notifications
- Resource-efficient
- Requires public server
- Not all services support it

### 4. Data Storage

**Database Design:**

```sql
-- Main filings table
CREATE TABLE filings (
    id INTEGER PRIMARY KEY,
    accession_number TEXT UNIQUE,
    ticker TEXT,
    company_name TEXT,
    filing_date TEXT,
    notified BOOLEAN
);

-- Tracking table
CREATE TABLE seen_entries (
    entry_id TEXT PRIMARY KEY,
    seen_at TIMESTAMP
);
```

**Best Practices:**
- Use UNIQUE constraints to prevent duplicates
- Index frequently queried fields (ticker, filing_date)
- Store raw data for debugging
- Use TIMESTAMP for tracking

### 5. Rate Limiting

**Implement Respectful Scraping:**

```python
class RateLimitedScraper:
    def __init__(self, requests_per_minute=30):
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = None

    @rate_limit
    def get(self, url):
        # Automatic rate limiting
        pass
```

**Guidelines:**
- Minimum 1 request per second
- Check for `Retry-After` headers
- Implement exponential backoff
- Use proper User-Agent

### 6. Legal Considerations

**✅ Legal:**
- Check robots.txt first
- Identify your bot clearly
- Use official APIs when available
- Respect rate limits
- Follow Terms of Service

**❌ Illegal:**
- Scrape behind authentication without permission
- Bypass CAPTCHA or anti-bot measures
- Scrape personal data without consent
- Ignore cease and desist orders

## Implementation

### Files Created

1. **Documentation**
   - `/docs/WEB_SCRAPING_GUIDE.md` - Complete guide with examples
   - `/scrapers/README.md` - Quick start for scrapers

2. **Backend Integration**
   - `/backend/routes/insider-trading.js` - Webhook endpoint for insider data
   - `/backend/server.js` - Updated to include new route

3. **Python Scraper**
   - `/scrapers/sec_monitor.py` - Full-featured SEC monitor
   - `/scrapers/requirements.txt` - Python dependencies

4. **Node.js Scraper**
   - `/scrapers/index.js` - Node.js version
   - `/scrapers/package.json` - Node dependencies

5. **Watchlists**
   - `/scrapers/watchlists/tech-stocks.txt` - Tech stocks
   - `/scrapers/watchlists/sp500-top10.txt` - S&P 500 top 10

## Quick Start

### 1. Install Dependencies

**Python:**
```bash
pip install aiohttp feedparser beautifulsoup4 lxml requests playwright python-dotenv
```

**Node.js:**
```bash
cd scrapers
npm install
```

### 2. Configure Environment

Create `.env` file:
```env
WEBHOOK_URL=http://localhost:3000/webhook/insider-trading
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. Start Webhook Server

```bash
npm start
```

### 4. Start Scraper

**Python:**
```bash
# Run once (test)
python scrapers/sec_monitor.py --once

# Continuous monitoring
python scrapers/sec_monitor.py --interval 30

# Monitor specific tickers
python scrapers/sec_monitor.py --ticker AAPL --ticker MSFT

# Use watchlist
python scrapers/sec_monitor.py --watchlist scrapers/watchlists/tech-stocks.txt
```

**Node.js:**
```bash
# Run once (test)
node scrapers/index.js --once

# Continuous monitoring
node scrapers/index.js --interval 30
```

## Usage Examples

### Monitor All Filings

```bash
python scrapers/sec_monitor.py --interval 30
```

### Monitor Specific Tickers

```bash
python scrapers/sec_monitor.py \
  --ticker AAPL \
  --ticker MSFT \
  --ticker GOOGL \
  --interval 15
```

### Use Watchlist File

```bash
python scrapers/sec_monitor.py \
  --watchlist scrapers/watchlists/tech-stocks.txt \
  --interval 30
```

### View Statistics

```bash
python scrapers/sec_monitor.py --stats
```

Output:
```
=== SEC Form 4 Monitor Statistics ===
Total filings: 1,234
Last 24 hours: 45

Top tickers:
  AAPL: 234
  MSFT: 189
  GOOGL: 156
```

## Integration with Your Stack

The scrapers integrate seamlessly with your existing trading webhook stack:

### 1. Webhook Endpoint

`POST /webhook/insider-trading`

**Request Body:**
```json
{
  "type": "insider_trading",
  "ticker": "AAPL",
  "company": "Apple Inc.",
  "insider": "Tim Cook",
  "transaction": "Purchase",
  "shares": "10,000",
  "price": "$180.50",
  "value": "$1,805,000",
  "filing_date": "2025-02-07",
  "url": "https://www.sec.gov/..."
}
```

### 2. Telegram Notifications

The webhook sends formatted messages to Telegram:

```
🟢 Insider Trading Alert

🏢 Company: Apple Inc.
📊 Ticker: AAPL
👤 Insider: Tim Cook
📈 Transaction: Purchase
📦 Shares: 10,000
💰 Price: $180.50
💵 Value: $1,805,000
📅 Date: 2025-02-07
🔗 View Filing

🕐 02/07/2025, 10:30:25
```

### 3. Dashboard Display

View all insider trading alerts at:
- `http://localhost:3000/dashboard`
- `http://localhost:3000/api/signals`

## Features

### Deduplication

The scrapers track seen filings to prevent duplicate alerts:

```python
# In-memory set for fast lookup
self.seen_entries = set()

# Database for persistence
CREATE TABLE seen_entries (
    entry_id TEXT PRIMARY KEY,
    seen_at TIMESTAMP
);
```

### Rate Limiting

Respectful scraping with configurable delays:

```python
# Check every 30 minutes
python sec_monitor.py --interval 30

# Or check every hour
python sec_monitor.py --interval 60
```

### Error Handling

Automatic retry with exponential backoff:

```python
@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_with_retry(url):
    return await session.get(url)
```

### Caching

Cache results to reduce load:

```python
class CachedScraper:
    def get_cached(self, url):
        # Check cache first
        cache_file = self.cache_dir / f"{hash(url)}.json"
        if cache_file.exists():
            return json.load(cache_file)

        # Fetch and cache
        data = self.fetch(url)
        self.set_cache(url, data)
        return data
```

## Advanced Usage

### Custom Webhook Handler

```python
class CustomWebhookHandler:
    async def send_to_webhook(self, data):
        # Enrich data
        data['sentiment'] = self.analyze_sentiment(data)

        # Send to multiple endpoints
        await asyncio.gather(
            self.send_to_trading_stack(data),
            self.send_to_slack(data),
            self.send_to_discord(data)
        )

monitor = SECForm4Monitor()
monitor.webhook_handler = CustomWebhookHandler()
```

### Filter Large Transactions

```python
def filter_large_transactions(filings, min_value=100000):
    """Only alert on transactions over $100K"""
    return [
        f for f in filings
        if float(f.get('value', 0)) > min_value
    ]
```

### Alert on Key Insiders

```python
KEY_INSIDERS = {
    'AAPL': ['Tim Cook', 'Luca Maestri'],
    'MSFT': ['Satya Nadella', 'Amy Hood']
}

def is_key_insider(filing):
    insiders = KEY_INSIDERS.get(filing['ticker'], [])
    return any(
        name.lower() in filing['insider'].lower()
        for name in insiders
    )
```

## Best Practices

### 1. Start Small

```bash
# Test with one ticker first
python sec_monitor.py --ticker AAPL --once

# Then scale up
python sec_monitor.py --watchlist tickers.txt
```

### 2. Monitor Resources

```bash
# Check logs
tail -f logs/insider-trading.log

# Check database size
ls -lh insider_trading.db
```

### 3. Set Alerts

- Monitor for scraper errors
- Track webhook delivery
- Watch for rate limiting
- Monitor database size

### 4. Respectful Scraping

- Use official RSS feeds when available
- Check robots.txt before scraping
- Implement proper rate limiting
- Identify your bot clearly
- Cache results aggressively

### 5. Legal Compliance

- Follow Terms of Service
- Don't scrape personal data
- Use official APIs when available
- Be transparent about your bot
- Respect cease and desist

## Troubleshooting

### No Webhooks Being Sent

1. Check webhook server is running:
```bash
curl http://localhost:3000/health
```

2. Check scraper logs:
```bash
python sec_monitor.py --once --debug
```

3. Verify webhook URL in `.env`

### Rate Limiting Errors

1. Increase interval:
```bash
python sec_monitor.py --interval 60
```

2. Monitor fewer tickers:
```bash
python sec_monitor.py --ticker AAPL
```

### Database Locked

1. Only run one instance:
```bash
ps aux | grep sec_monitor
```

2. Close other connections:
```bash
lsof insider_trading.db
```

## Resources

- **SEC EDGAR API**: https://www.sec.gov/edgar/sec-api-documentation
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Playwright Docs**: https://playwright.dev/
- **Puppeteer Docs**: https://pptr.dev/
- **Python requests**: https://docs.python-requests.org/

## Next Steps

1. **Test the scrapers** with `--once` flag
2. **Configure your watchlist** with interesting tickers
3. **Set up monitoring** for errors and performance
4. **Integrate with trading strategy** based on insider data
5. **Scale up** gradually with more tickers

## Disclaimer

This tool is for informational purposes only. Always verify data from official sources. Comply with all applicable laws and website terms of service. Insider trading data should be used as one of many factors in investment decisions, not as the sole basis.

## License

MIT
