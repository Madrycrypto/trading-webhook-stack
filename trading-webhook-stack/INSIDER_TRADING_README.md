# Insider Trading Data Fetcher

A comprehensive Python tool for fetching and analyzing SEC Form 4 insider trading data for US stocks.

## Features

- ✅ Fetch SEC Form 4 filings for any US stock
- ✅ Parse XML filing data to extract transaction details
- ✅ Generate trading signals (STRONG_BUY, BUY, NEUTRAL, SELL, STRONG_SELL)
- ✅ Batch processing for multiple tickers
- ✅ Export to CSV
- ✅ Configurable rate limiting
- ✅ No API key required (SEC EDGAR is free)

## Installation

```bash
# Clone or download this repository
cd trading-webhook-stack

# Install required packages
pip install requests pandas

# Or use pip with requirements file
pip install -r requirements.txt
```

## Quick Start

### 1. Basic Usage - Single Ticker

```bash
# Get recent Form 4 filings for Apple (last 30 days)
python insider_trading_fetcher.py --ticker AAPL

# Get filings for last 7 days
python insider_trading_fetcher.py --ticker AAPL --days 7
```

### 2. Get Detailed Transaction Data

```bash
# Fetch detailed transaction information
python insider_trading_fetcher.py --ticker AAPL --details

# With signals
python insider_trading_fetcher.py --ticker AAPL --details --signals
```

### 3. Multiple Tickers

```bash
# Fetch multiple stocks
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL,TSLA --details --signals

# Look back 60 days
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --days 60 --details --signals
```

### 4. Export to CSV

```bash
# Save results to CSV
python insider_trading_fetcher.py --ticker AAPL --details --signals --output aapl_insider_trades.csv

# Multiple tickers to CSV
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals --output insider_trades.csv
```

## Output Examples

### Basic Output (Filings Only)

```
Fetching filings for AAPL (CIK: 0000320193)...
✓ Found 5 Form 4 filings for AAPL in last 30 days

Results
=======
ticker       cik         accession_number          filing_date         report_date
AAPL  0000320193  0000320193-26-000001  2026-02-05 00:00:00  2026-02-03
AAPL  0000320193  0000320193-26-000002  2026-02-01 00:00:00  2026-01-30
...
```

### Detailed Output with Transactions

```
Processing AAPL...
✓ Found 5 Form 4 filings for AAPL in last 30 days
  Downloading 0000320193-26-000001...
  Downloading 0000320193-26-000002...
✓ Extracted 8 transactions from 5 filings

Generating trading signals...
====================

Signal Summary:
BUY            5
NEUTRAL        2
STRONG_BUY     1

Results
=======
ticker  filing_date  insider_name       position       transaction_type  shares   total_value    signal
AAPL   2026-02-05   Tim Cook           CEO            Purchase         10000   1500000.00   STRONG_BUY
AAPL   2026-02-05   Luca Maestri       CFO            Purchase          5000    750000.00    BUY
...
```

## Signal Explanation

The analyzer generates signals based on multiple factors:

### Signal Levels

- **STRONG_BUY** 🚀🚀🚀 - Multiple bullish factors aligned
  - Large purchase by CEO/CFO
  - >$1M transaction value
  - Significant ownership increase

- **BUY** 🚀 - Bullish indicators present
  - Purchase by executive/director
  - >$100k transaction value
  - Moderate ownership increase

- **NEUTRAL** ➡️ - No clear directional signal
  - Small transactions
  - Awards/grants
  - Mixed signals

- **SELL** ⚠️ - Bearish indicators
  - Sales by executives
  - Large percentage sales

- **STRONG_SELL** 🔴🔴🔴 - Strong bearish signals
  - Large CEO/CFO sales
  - Significant ownership decrease

### Signal Calculation

Signals are calculated using a scoring system:

```python
# Transaction Type
- Purchase (P): +2 points
- Sale (S): -1 point
- Award (A): +1 point

# Transaction Size
- >$1M: +2 points
- >$100k: +1 point

# Position
- CEO/CFO: +2 points
- Director: +1 point

# Total Score
- ≥5: STRONG_BUY
- ≥3: BUY
- ≥0: NEUTRAL
- ≥-2: SELL
- <-2: STRONG_SELL
```

## Configuration

### User-Agent (Required)

The SEC requires a User-Agent header. Customize this:

```bash
python insider_trading_fetcher.py --ticker AAPL \
    --user-agent "Your Name (your.email@example.com)"
```

### Rate Limiting

The tool automatically respects SEC rate limits:
- Default: 5 requests per second
- Automatic delays between requests
- Recommended for production use

## Integration with Trading Systems

### Example 1: Filter Based on Insider Sentiment

```python
# In your Oneshot FTMO system
from insider_trading_fetcher import SECInsiderTrading, InsiderSignalAnalyzer

sec = SECInsiderTrading()
df = sec.get_insider_trading('AAPL', days_back=7, fetch_details=True)

if not df.empty:
    df = InsiderSignalAnalyzer.analyze_dataframe(df)

    # Only take LONG signals if recent insider buying
    recent_buys = df[
        (df['transaction_code'] == 'P') &
        (df['signal'].isin(['BUY', 'STRONG_BUY']))
    ]

    if len(recent_buys) > 0:
        print(f"✓ Insider buying detected: {len(recent_buys)} purchases")
        # Allow long trades
    else:
        print("✗ No recent insider buying - skip trade")
```

### Example 2: Stock Selection

```python
# Select stocks with strongest insider buying
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']

best_stocks = []
for ticker in tickers:
    df = sec.get_insider_trading(ticker, days_back=30, fetch_details=True)
    if not df.empty:
        df = InsiderSignalAnalyzer.analyze_dataframe(df)

        strong_buys = df[df['signal'] == 'STRONG_BUY']
        if len(strong_buys) > 0:
            total_value = strong_buys['total_value'].sum()
            best_stocks.append({
                'ticker': ticker,
                'strong_buy_count': len(strong_buys),
                'total_value': total_value
            })

# Sort by total insider buying value
best_stocks = sorted(best_stocks, key=lambda x: x['total_value'], reverse=True)

print("Top insider buying stocks:")
for stock in best_stocks[:3]:
    print(f"  {stock['ticker']}: ${stock['total_value']:,.0f}")
```

### Example 3: Telegram Alerts

```python
import requests

def send_telegram_alert(signal_data):
    """Send insider trading signal to Telegram"""
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"

    emoji = {
        'STRONG_BUY': '🚀🚀🚀',
        'BUY': '🚀',
        'NEUTRAL': '➡️',
        'SELL': '⚠️',
        'STRONG_SELL': '🔴🔴🔴'
    }

    message = f"""
🔔 <b>Insider Trading Alert</b>

{emoji.get(signal_data['signal'], '📊')} <b>Signal:</b> {signal_data['signal']}

<b>Ticker:</b> {signal_data['ticker']}
<b>Insider:</b> {signal_data['insider_name']}
<b>Position:</b> {signal_data['position']}

<b>Transaction:</b>
• Type: {signal_data['transaction_type']}
• Shares: {signal_data['shares']:,.0f}
• Value: ${signal_data['total_value']:,.2f}
• Date: {signal_data['transaction_date']}
"""

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    requests.post(url, json=data)

# Usage
for _, row in df.iterrows():
    if row['signal'] in ['STRONG_BUY', 'BUY']:
        send_telegram_alert(row.to_dict())
```

## Data Columns

### Basic Filings Data
- `ticker` - Stock symbol
- `cik` - SEC Central Index Key (10 digits)
- `accession_number` - Unique filing identifier
- `filing_date` - When filed with SEC
- `report_date` - Transaction date

### Detailed Transaction Data
- `insider_name` - Name of insider
- `position` - Title/position (CEO, CFO, Director, etc.)
- `transaction_date` - Date of transaction
- `transaction_code` - P (Purchase), S (Sale), A (Award), etc.
- `transaction_type` - Description of transaction type
- `shares` - Number of shares traded
- `price_per_share` - Execution price
- `total_value` - Total transaction value (shares × price)
- `shares_owned_after` - Total shares owned after transaction
- `signal` - Generated signal (if --signals flag used)

## Transaction Codes

| Code | Description | Sentiment |
|------|-------------|-----------|
| P | Open market purchase | Bullish |
| S | Open market sale | Bearish |
| M | Multiple transactions | Neutral |
| A | Grant/Award (stock, option) | Neutral-Bullish |
| D | Sale to issuer | Bearish |
| F | Payment of exercise price | Neutral |
| G | Gift | Neutral |
| X | Option exercise | Neutral |

## Best Practices

### 1. Respect Rate Limits
```bash
# SEC allows ~10 requests per second
# Tool defaults to 5 per second for safety
# Don't modify rate limiting unless necessary
```

### 2. Use Proper User-Agent
```bash
# Include your email in User-Agent
--user-agent "Your Name (your.email@example.com)"
```

### 3. Cache Results
```python
# Store results locally to avoid refetching
df.to_csv('insider_data_cache.csv', index=False)
```

### 4. Filter Meaningful Transactions
```python
# Focus on significant trades
meaningful = df[
    (df['total_value'] > 50000) &  # >$50k
    (df['transaction_code'].isin(['P', 'S']))  # Purchases/Sales only
]
```

### 5. Consider Position and Size
```python
# CEO purchases are more significant than director sales
weight = 1.0
if 'CEO' in position:
    weight = 2.0
elif 'CFO' in position:
    weight = 1.5
```

## Troubleshooting

### "Ticker not found"
- Check ticker symbol is correct
- Ensure it's a US public company
- Run without --details flag first to verify CIK

### "No Form 4 filings found"
- Normal for some companies with low insider activity
- Try increasing --days parameter
- Verify company has insiders who must file

### "Error downloading Form 4"
- Network connectivity issue
- SEC server temporarily unavailable
- Wait and retry

### Rate Limiting Issues
- Reduce batch size
- Increase delay between requests
- Cache results locally

## Data Source Information

- **Source**: SEC EDGAR (Electronic Data Gathering, Analysis, and Retrieval)
- **Update Frequency**: Real-time as filings are submitted
- **Coverage**: All US publicly traded companies
- **Cost**: Free
- **Rate Limit**: 10 requests per second per IP
- **Documentation**: https://www.sec.gov/edgar/sec-api-documentation

## Legal & Compliance Notes

✅ **Legal to Use**: SEC Form 4 data is public information
✅ **Not Insider Trading**: Using public filings is not insider trading
✅ **Free Access**: No API key or payment required
⚠️ **Verify Data**: Errors can occur in filings
⚠️ **Respect Limits**: Essential for continued access
⚠️ **Cite Sources**: When distributing data

## Advanced Usage

### Database Integration

```python
import psycopg2
from insider_trading_fetcher import SECInsiderTrading

# Store in PostgreSQL
conn = psycopg2.connect(
    dbname='insider_trading',
    user='postgres',
    password='password',
    host='localhost'
)

# Fetch and store
sec = SECInsiderTrading()
df = sec.get_insider_trading('AAPL', days_back=30, fetch_details=True)

# Save to database
df.to_sql('insider_transactions', conn, if_exists='append', index=False)
```

### Automated Monitoring

```python
# Run daily to monitor watchlist
import schedule
import time

def daily_check():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    sec = SECInsiderTrading()

    for ticker in tickers:
        df = sec.get_insider_trading(ticker, days_back=1, fetch_details=True)

        if not df.empty:
            strong_buys = df[df['signal'] == 'STRONG_BUY']
            if len(strong_buys) > 0:
                send_telegram_alert(f"Strong insider buying in {ticker}")

# Schedule daily check at 9 AM
schedule.every().day.at("09:00").do(daily_check)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

## Contributing

This tool is part of the Oneshot FTMO trading system. For updates and improvements:

1. Check for SEC API changes
2. Test with new tickers
3. Improve signal accuracy
4. Add more data sources

## Support

For issues or questions:
- Review SEC EDGAR documentation
- Check ticker symbols
- Verify network connectivity
- Review rate limiting settings

## Version History

- **v1.0** (2026-02-06) - Initial release
  - SEC EDGAR integration
  - Form 4 parsing
  - Signal generation
  - Batch processing
  - CSV export

## License

This tool is provided as-is for educational and trading purposes.

---

**Remember**: Insider trading data is just one factor. Always combine with other analysis methods and proper risk management.
