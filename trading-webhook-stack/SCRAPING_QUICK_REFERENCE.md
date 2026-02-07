# Web Scraping Quick Reference

## Essential Commands

### Start Webhook Server
```bash
npm start
```

### Test Webhook Endpoint
```bash
node scrapers/test.js
```

### Run Scraper Once (Test)
```bash
# Python
python scrapers/sec_monitor.py --once

# Node.js
node scrapers/index.js --once
```

### Start Continuous Monitoring
```bash
# Python - All filings
python scrapers/sec_monitor.py --interval 30

# Python - Specific tickers
python scrapers/sec_monitor.py --ticker AAPL --ticker MSFT --interval 15

# Python - Watchlist
python scrapers/sec_monitor.py --watchlist scrapers/watchlists/tech-stocks.txt --interval 30

# Node.js
node scrapers/index.js --interval 30
```

### View Statistics
```bash
python scrapers/sec_monitor.py --stats
```

## Webhook Endpoints

### Insider Trading Webhook
```
POST /webhook/insider-trading
Content-Type: application/json

{
  "type": "insider_trading",
  "ticker": "AAPL",
  "company": "Apple Inc.",
  "filing_date": "2025-02-07",
  "url": "https://www.sec.gov/...",
  "timestamp": "2025-02-07T10:30:00Z"
}
```

### Batch Insider Trading
```
POST /webhook/insider-trading/batch
Content-Type: application/json

{
  "transactions": [
    { "ticker": "AAPL", "company": "Apple Inc.", ... },
    { "ticker": "MSFT", "company": "Microsoft", ... }
  ]
}
```

## File Structure

```
trading-webhook-stack/
├── backend/
│   ├── routes/
│   │   └── insider-trading.js      # Webhook endpoint
│   └── server.js                   # Updated with new route
├── scrapers/
│   ├── index.js                    # Node.js scraper
│   ├── sec_monitor.py              # Python scraper
│   ├── package.json                # Node dependencies
│   ├── requirements.txt            # Python dependencies
│   ├── test.js                     # Test script
│   ├── README.md                   # Scraper documentation
│   └── watchlists/
│       ├── tech-stocks.txt         # Tech stocks watchlist
│       └── sp500-top10.txt         # S&P 500 top 10
├── docs/
│   └── WEB_SCRAPING_GUIDE.md       # Complete guide
└── WEB_SCRAPING_SUMMARY.md         # Summary and overview
```

## Environment Variables

Create `.env` file in root directory:

```env
# Webhook configuration
WEBHOOK_URL=http://localhost:3000/webhook/insider-trading

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Server configuration
PORT=3000
```

## Common Tasks

### Install Dependencies

**Python:**
```bash
pip install aiohttp feedparser beautifulsoup4 lxml requests playwright python-dotenv
```

**Node.js:**
```bash
cd scrapers
npm install
```

### Create Custom Watchlist

Create `my-watchlist.txt`:
```
# My favorite stocks
AAPL  # Apple
MSFT  # Microsoft
GOOGL # Google
```

Run with watchlist:
```bash
python scrapers/sec_monitor.py --watchlist my-watchlist.txt --interval 30
```

### Monitor for Large Transactions

Edit `sec_monitor.py` and add filter:

```python
def filter_large_transactions(filings, min_value=100000):
    """Only alert on transactions over $100K"""
    return [
        f for f in filings
        if float(f.get('value', 0)) > min_value
    ]

# Use in processing loop
large_filings = filter_large_transactions(entries, min_value=100000)
await self.process_entries(large_filings, notify=True)
```

### Run as Background Service

**Using PM2 (Node.js):**
```bash
pm2 start scrapers/index.js --name insider-scraper
pm2 logs insider-scraper
pm2 status
```

**Using systemd (Python):**
```bash
# Create service file: /etc/systemd/system/insider-monitor.service
sudo systemctl start insider-monitor
sudo systemctl enable insider-monitor
sudo systemctl status insider-monitor
```

**Using screen/tmux:**
```bash
screen -S insider-monitor
python scrapers/sec_monitor.py --interval 30
# Press Ctrl+A, D to detach
screen -r insider-monitor  # Reattach
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env
PORT=3001
```

### Database Locked
```bash
# Only run one instance at a time
ps aux | grep sec_monitor
kill <PID>
```

### No Telegram Messages
```bash
# Check token and chat ID in .env
# Test bot: /start message to @YourBot
```

### Rate Limiting
```bash
# Increase interval between checks
python sec_monitor.py --interval 60
```

## Monitoring and Logs

### View Scraper Logs
```bash
# Python
tail -f logs/insider-trading.log

# Node.js (PM2)
pm2 logs insider-scraper

# Systemd
sudo journalctl -u insider-monitor -f
```

### Check Webhook Delivery
```bash
# Check webhook logs
tail -f logs/webhook.log

# View database
sqlite3 insider_trading.db "SELECT COUNT(*) FROM filings;"
sqlite3 insider_trading.db "SELECT * FROM filings ORDER BY created_at DESC LIMIT 10;"
```

## Performance Tips

1. **Use watchlists** instead of scraping all filings
2. **Increase interval** to reduce server load
3. **Use Python async** for better concurrency
4. **Cache results** to avoid duplicate work
5. **Monitor database size** and archive old data

## Security Best Practices

1. **Use .env file** for sensitive data
2. **Don't commit .env** to git
3. **Use HTTPS** in production
4. **Implement authentication** on webhooks
5. **Validate all input** data
6. **Rate limit webhook calls**
7. **Monitor for abuse**

## Legal Compliance

✅ **DO:**
- Check robots.txt before scraping
- Use official APIs when available
- Identify your bot with User-Agent
- Respect rate limits
- Follow Terms of Service

❌ **DON'T:**
- Scrape behind authentication
- Bypass CAPTCHA/anti-bot
- Scrape personal data
- Ignore cease and desist
- Overload servers

## Quick Test

Test entire stack:
```bash
# Terminal 1: Start webhook server
npm start

# Terminal 2: Test webhook
node scrapers/test.js

# Terminal 3: Run scraper once
python scrapers/sec_monitor.py --once
```

## Getting Help

1. Check logs: `tail -f logs/*.log`
2. Test webhook: `node scrapers/test.js`
3. View stats: `python sec_monitor.py --stats`
4. Read docs: `/docs/WEB_SCRAPING_GUIDE.md`
5. Check README: `/scrapers/README.md`

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure .env file
3. ✅ Start webhook server
4. ✅ Test webhook endpoint
5. ✅ Run scraper once
6. ✅ Set up continuous monitoring
7. ✅ Create custom watchlist
8. ✅ Monitor and adjust settings
