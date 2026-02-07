# Insider Trading Data - Quick Reference Guide

## One-Line Commands

```bash
# Install dependencies
pip install requests pandas

# Fetch recent filings for Apple
python insider_trading_fetcher.py --ticker AAPL

# Get detailed transactions with signals
python insider_trading_fetcher.py --ticker AAPL --details --signals

# Multiple stocks
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals

# Export to CSV
python insider_trading_fetcher.py --ticker AAPL --details --signals --output aapl.csv
```

## Quick Python Examples

### 1. Basic Fetch
```python
from insider_trading_fetcher import SECInsiderTrading

sec = SECInsiderTrading()
df = sec.get_insider_trading('AAPL', days_back=30, fetch_details=True)
print(df)
```

### 2. Generate Signals
```python
from insider_trading_fetcher import SECInsiderTrading, InsiderSignalAnalyzer

sec = SECInsiderTrading()
df = sec.get_insider_trading('AAPL', days_back=30, fetch_details=True)
df = InsiderSignalAnalyzer.analyze_dataframe(df)

# Show strong buys
strong_buys = df[df['signal'] == 'STRONG_BUY']
print(strong_buys)
```

### 3. Check Before Trading
```python
def check_insider_sentiment(ticker):
    sec = SECInsiderTrading()
    df = sec.get_insider_trading(ticker, days_back=7, fetch_details=True)

    if df.empty:
        return "No data"

    df = InsiderSignalAnalyzer.analyze_dataframe(df)
    recent_buys = df[df['transaction_code'] == 'P']

    if len(recent_buys) > 0:
        return f"BULLISH: {len(recent_buys)} purchases"
    else:
        return "No recent buying"

# Usage
print(check_insider_sentiment('AAPL'))
```

### 4. Find Best Opportunities
```python
sec = SECInsiderTrading()
tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA']

for ticker in tickers:
    df = sec.get_insider_trading(ticker, days_back=30, fetch_details=True)
    if not df.empty:
        df = InsiderSignalAnalyzer.analyze_dataframe(df)
        strong_buys = len(df[df['signal'] == 'STRONG_BUY'])
        if strong_buys > 0:
            print(f"{ticker}: {strong_buys} strong buy signals")
```

## Key URLs

### US Market
- SEC EDGAR: https://www.sec.gov/Archives/edgar/data/
- Company Tickers: https://www.sec.gov/files/company_tickers.json
- OpenInsider: https://openinsider.com/
- Finviz Insider: https://finviz.com/insidertrading.ashx

### European Market
- UK (FCA): https://www.disclosures.org.uk/
- Germany (BaFin): https://www.bafin.de/
- France (AMF): https://www.amf-france.org/

### Polish Market
- KNF ESPI: https://www.knf.gov.pl/en/menu/5/information-disp-layed-in-espi
- Bankier.pl: https://www.bankier.pl/gielda/notyfikacje

## Signal Quick Guide

| Signal | Meaning | Action |
|--------|---------|--------|
| 🚀🚀🚀 STRONG_BUY | CEO/CFO bought >$1M | Consider LONG |
| 🚀 BUY | Executive bought >$100k | Bullish |
| ➡️ NEUTRAL | Mixed signals | No action |
| ⚠️ SELL | Executive selling | Bearish |
| 🔴🔴🔴 STRONG_SELL | CEO sold large % | Avoid/SHORT |

## Transaction Codes

| Code | Type | Sentiment |
|------|------|-----------|
| P | Purchase | Bullish ✅ |
| S | Sale | Bearish ⚠️ |
| A | Award/Grant | Neutral |
| X | Option Exercise | Neutral |

## Important Thresholds

| Region | Min Report | Deadline |
|--------|-----------|----------|
| US | $10,000 | 2 days |
| EU | €5,000 | 3 days |
| Poland | PLN 20,000 | 3 days |

## Data Points Explained

### Required Columns
- `ticker` - Stock symbol (AAPL)
- `insider_name` - Person who traded
- `position` - CEO, CFO, Director, etc.
- `transaction_code` - P=Purchase, S=Sale
- `shares` - Number of shares traded
- `total_value` - Total dollar amount
- `transaction_date` - When trade happened
- `signal` - BUY/SELL/NEUTRAL

### Optional Columns
- `filing_date` - When reported to SEC
- `price_per_share` - Execution price
- `shares_owned_after` - Total holdings after trade

## Common Filters

### Bullish Signals
```python
# Recent insider purchases
bullish = df[
    (df['transaction_code'] == 'P') &  # Purchases only
    (df['total_value'] > 100000) &     # >$100k
    (df['signal'].isin(['BUY', 'STRONG_BUY']))
]
```

### C-Level Executives
```python
# CEO/CFO/CTO trades
execs = df[df['position'].str.contains('CEO|CFO|CTO|Chief', case=False)]
```

### Large Transactions
```python
# >$500k trades
large = df[df['total_value'] > 500000]
```

### Recent Activity
```python
# Last 7 days
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=7)
recent = df[pd.to_datetime(df['transaction_date']) >= cutoff]
```

## Rate Limits

### SEC EDGAR
- **Limit**: 10 requests/second
- **Tool default**: 5 requests/second (safe)
- **Required**: User-Agent header

### Best Practice
```python
# Always set User-Agent
headers = {
    'User-Agent': 'Your Name (your.email@example.com)'
}

# Add delay between requests
import time
time.sleep(0.2)  # 5 per second
```

## Export Options

### CSV
```python
df.to_csv('insider_trades.csv', index=False)
```

### Excel
```python
df.to_excel('insider_trades.xlsx', index=False)
```

### JSON
```python
df.to_json('insider_trades.json', orient='records')
```

## Integration with Trading Systems

### Oneshot FTMO Filter
```python
def oneshot_insider_filter(ticker):
    """Check insider sentiment before trade"""
    sec = SECInsiderTrading()
    df = sec.get_insider_trading(ticker, days_back=7, fetch_details=True)

    if df.empty:
        return True  # No data, skip filter

    df = InsiderSignalAnalyzer.analyze_dataframe(df)

    # Only trade if insider buying
    return df[df['transaction_code'] == 'P']['signal'].isin(['BUY', 'STRONG_BUY']).any()

# Usage in trading system
if oneshot_insider_filter('XAUUSD'):
    # Allow trade
    pass
```

### Telegram Alert
```python
def send_insider_alert(transaction):
    import requests

    bot_token = "YOUR_TOKEN"
    chat_id = "YOUR_CHAT_ID"

    message = f"""
🔔 Insider Alert
{transaction['ticker']}: {transaction['signal']}
{transaction['insider_name']} ({transaction['position']})
{transaction['transaction_type']}: {transaction['shares']} shares
Value: ${transaction['total_value']:,.2f}
"""

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={'chat_id': chat_id, 'text': message})
```

## Troubleshooting

### "Ticker not found"
- Check ticker is correct (AAPL not aapl)
- Ensure it's a US public company
- Run without --details first

### "No Form 4 filings"
- Normal for some companies
- Try increasing --days to 60 or 90
- Company may have low insider activity

### "Error downloading"
- Network issue
- SEC temporarily unavailable
- Wait and retry

### Rate limited
- Tool handles automatically
- Reduce batch size
- Wait longer between runs

## File Locations

```
trading-webhook-stack/
├── insider-trading-data-guide.md          # Complete guide (14,000 words)
├── INSIDER_TRADING_README.md              # User documentation
├── INSIDER_TRADING_SUMMARY.md             # Project summary
├── INSIDER_TRADING_QUICK_REFERENCE.md     # This file
├── insider_trading_fetcher.py             # Main tool
├── example_insider_trading.py             # 7 examples
├── requirements-insider-trading.txt       # Dependencies
└── insider_trading_config.example.json    # Config template
```

## Quick Start (5 minutes)

```bash
# 1. Install
pip install requests pandas

# 2. Run example
python example_insider_trading.py

# 3. Fetch your first data
python insider_trading_fetcher.py --ticker AAPL --details --signals

# 4. Check the output
# You'll see insider transactions with signals

# 5. Export to CSV
python insider_trading_fetcher.py --ticker AAPL --details --signals --output my_trades.csv
```

## Next Steps

1. **Read**: `INSIDER_TRADING_README.md` for detailed usage
2. **Run**: `example_insider_trading.py` to see examples
3. **Configure**: Copy `insider_trading_config.example.json` to your config
4. **Integrate**: Add insider filter to your trading system
5. **Monitor**: Set up daily checks with cron/task scheduler

## Common Use Cases

### Daily Monitoring
```bash
# Check every morning
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals
```

### Stock Selection
```python
# Find best insider buying stocks
# See example_insider_trading.py Example 5
```

### Pre-Trade Check
```python
# Verify insider sentiment before opening position
# See example_insider_trading.py Example 3
```

### Automated Alerts
```python
# Send Telegram alerts for strong signals
# Set up cron job to run daily
```

## Support

- **Documentation**: See `insider-trading-data-guide.md`
- **Examples**: Run `example_insider_trading.py`
- **Issues**: Check troubleshooting section
- **API Docs**: https://www.sec.gov/edgar/sec-api-documentation

---

**Remember**: Insider trading data is public information and legal to use. Always combine with other analysis and proper risk management.

**Last Updated**: February 6, 2026
**Version**: 1.0
