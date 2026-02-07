# Insider Trading Scrapers

Production-ready scrapers for monitoring SEC Form 4 insider trading disclosures with webhook integration.

## Features

- **Multiple scraping methods**: RSS feeds, Puppeteer, BeautifulSoup
- **Rate limiting**: Respectful scraping with configurable delays
- **Webhook integration**: Send alerts to your existing trading webhook stack
- **Telegram notifications**: Optional Telegram alerts for new filings
- **Database storage**: SQLite for tracking and history
- **Deduplication**: Never send duplicate alerts
- **Continuous monitoring**: Cron-based scheduling
- **Watchlist support**: Monitor specific tickers or all filings

## Quick Start

### Python Version

1. **Install dependencies:**
```bash
cd scrapers
pip install -r requirements.txt
```

2. **Run once (test):**
```bash
python sec_monitor.py --once
```

3. **Run continuous monitoring:**
```bash
python sec_monitor.py --interval 30
```

4. **Monitor specific tickers:**
```bash
python sec_monitor.py --ticker AAPL --ticker MSFT --interval 15
```

5. **Use watchlist file:**
```bash
echo "AAPL\nMSFT\nGOOGL\nTSLA" > tickers.txt
python sec_monitor.py --watchlist tickers.txt --interval 30
```

### Node.js Version

1. **Install dependencies:**
```bash
cd scrapers
npm install
```

2. **Run once (test):**
```bash
node index.js --once
```

3. **Run continuous monitoring:**
```bash
node index.js --interval 30
```

4. **Monitor specific tickers:**
```bash
node index.js --ticker AAPL --ticker MSFT --interval 15
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Webhook URL (your existing trading webhook stack)
WEBHOOK_URL=http://localhost:3000/webhook/insider-trading

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--ticker <SYMBOL>` | Add ticker to monitor | All tickers |
| `--watchlist <FILE>` | Load tickers from file | - |
| `--interval <MINUTES>` | Check interval | 30 |
| `--once` | Run once and exit | - |
| `--stats` | Show statistics | - |
| `--webhook <URL>` | Custom webhook URL | localhost:3000 |
| `--db <PATH>` | Database path | insider_trading.db |

## Webhook Integration

The scrapers send data to your existing webhook endpoint:

```json
{
  "type": "insider_trading",
  "ticker": "AAPL",
  "company": "Apple Inc.",
  "filing_date": "2025-02-07",
  "url": "https://www.sec.gov/...",
  "timestamp": "2025-02-07T10:30:00Z"
}
```

Your webhook endpoint at `/webhook/insider-trading` will:

1. Receive the insider trading data
2. Store in database
3. Send Telegram notification
4. Display on dashboard

## Database Schema

### SQLite Database (Python)

```sql
-- Filings table
CREATE TABLE filings (
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
);

-- Seen entries tracking
CREATE TABLE seen_entries (
    entry_id TEXT PRIMARY KEY,
    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Monitoring Strategies

### 1. Polling (Recommended)

**Advantages:**
- Simple to implement
- Works with most websites
- Control over frequency

**Disadvantages:**
- Can miss rapid updates
- Uses resources continuously

**Implementation:**
```python
# Check every 30 minutes
python sec_monitor.py --interval 30
```

### 2. RSS Feeds (Best for SEC)

**Advantages:**
- Official data source
- No scraping needed
- Real-time updates

**Implementation:**
```python
# Built into sec_monitor.py
monitor = SECForm4Monitor()
await monitor.fetch_sec_rss(tickers=['AAPL'])
```

### 3. Push-Based (Webhooks)

**Advantages:**
- Instant notifications
- Resource-efficient

**Disadvantages:**
- Requires public server
- Not all services support it

## Rate Limiting

### Respectful Scraping Guidelines

1. **Check robots.txt:**
```bash
curl https://www.sec.gov/robots.txt
```

2. **Identify your bot:**
```python
headers = {
    'User-Agent': 'InsiderTradingMonitor/1.0 (contact: your-email@example.com)'
}
```

3. **Implement delays:**
```python
# Minimum 1 second between requests
time.sleep(1)
```

4. **Exponential backoff on errors:**
```python
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_with_retry(url):
    return requests.get(url)
```

## Examples

### Monitor Multiple Tickers

```bash
python sec_monitor.py \
  --ticker AAPL \
  --ticker MSFT \
  --ticker GOOGL \
  --ticker TSLA \
  --ticker NVDA \
  --interval 15
```

### Use Watchlist File

Create `tickers.txt`:
```
# Tech stocks
AAPL
MSFT
GOOGL
META
NVDA

# Pharma
PFE
JNJ
MRNA
```

Run:
```bash
python sec_monitor.py --watchlist tickers.txt --interval 30
```

### View Statistics

```bash
python sec_monitor.py --stats
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
  TSLA: 142
  NVDA: 98
```

## Integration with Trading Webhook Stack

### 1. Start the webhook server:

```bash
cd /path/to/trading-webhook-stack
npm start
```

### 2. Start the scraper:

```bash
python scrapers/sec_monitor.py --interval 30
```

### 3. Receive alerts:

- **Dashboard**: View at `http://localhost:3000/dashboard`
- **Telegram**: Get instant notifications
- **API**: Query at `http://localhost:3000/api/signals`

## Troubleshooting

### No webhooks being sent

1. Check webhook server is running:
```bash
curl http://localhost:3000/health
```

2. Check scraper logs:
```bash
python sec_monitor.py --once --debug
```

3. Verify webhook URL in `.env`

### Rate limiting errors

1. Increase interval:
```bash
python sec_monitor.py --interval 60
```

2. Monitor fewer tickers:
```bash
python sec_monitor.py --ticker AAPL
```

### Database locked errors

1. Only run one instance at a time
2. Check for existing processes:
```bash
ps aux | grep sec_monitor
```

## Legal Considerations

### ✅ Legal Practices

1. **Check robots.txt** before scraping
2. **Identify your bot** with proper User-Agent
3. **Respect rate limits** (1 req/sec minimum)
4. **Use official APIs** when available (SEC EDGAR API)
5. **Follow Terms of Service**

### ❌ Illegal Practices

1. **Scraping behind authentication** without permission
2. **Bypassing CAPTCHA** or anti-bot measures
3. **Scraping personal data** without consent
4. **Ignoring cease and desist** orders

### Best Practices

- Use SEC's official RSS feeds (no scraping needed)
- Implement proper caching
- Don't overload servers
- Monitor for errors
- Be transparent about your bot

## Advanced Usage

### Custom Webhook Handler

```python
class CustomWebhookHandler:
    async def send_to_webhook(self, data):
        # Add custom logic
        enriched_data = self.enrich_data(data)

        # Send to multiple endpoints
        await self.send_to_trading_stack(enriched_data)
        await self.send_to_slack(enriched_data)
        await self.send_to_discord(enriched_data)

monitor = SECForm4Monitor(webhook_url=CustomWebhookHandler())
```

### Filter Large Transactions

```python
def filter_large_transactions(filings, min_value=100000):
    """Filter only transactions over $100K"""
    return [
        f for f in filings
        if float(f.get('value', 0)) > min_value
    ]

filtered = filter_large_transactions(filings)
```

### Alert on Specific Insiders

```python
KEY_INSIDERS = {
    'AAPL': ['Tim Cook', 'Luca Maestri'],
    'MSFT': ['Satya Nadella', 'Amy Hood']
}

def is_key_insider(filing):
    insiders = KEY_INSIDERS.get(filing['ticker'], [])
    return any(name.lower() in filing['insider'].lower()
               for name in insiders)
```

## Performance Tips

1. **Use async I/O** for concurrent requests
2. **Cache results** to avoid duplicate work
3. **Batch webhook requests** for efficiency
4. **Use database indexes** for faster queries
5. **Monitor memory usage** with large datasets

## Support

For issues or questions:

1. Check logs: `logs/insider-trading.log`
2. Verify configuration: Check `.env` file
3. Test webhook: Use `--once` flag
4. View stats: Use `--stats` flag

## License

MIT

## Disclaimer

This tool is for informational purposes only. Always verify data from official sources. Comply with all applicable laws and website terms of service.
