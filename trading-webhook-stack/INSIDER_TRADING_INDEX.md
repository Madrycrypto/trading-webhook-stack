# Insider Trading Data Sources - Complete Package

**Created:** February 6, 2026
**Version:** 1.0
**Author:** Trading Webhook Stack

---

## Package Overview

This package provides a comprehensive solution for fetching, analyzing, and utilizing insider trading data from SEC Form 4 filings. It includes documentation, production-ready code, examples, and integration guides.

**Key Features:**
- ✅ Free SEC EDGAR API integration (no API key required)
- ✅ Automatic Form 4 parsing and signal generation
- ✅ Batch processing for multiple stocks
- ✅ CSV export functionality
- ✅ Telegram alert integration
- ✅ Ready for integration with Oneshot FTMO system

---

## Quick Start (5 Minutes)

```bash
# 1. Install dependencies
pip install requests pandas

# 2. Run the fetcher
python insider_trading_fetcher.py --ticker AAPL --details --signals

# 3. View results
# You'll see insider transactions with trading signals
```

---

## Package Contents

### 📚 Documentation Files (5 files)

#### 1. **insider-trading-data-guide.md** (14,000+ words)
**Complete reference guide covering:**
- US SEC EDGAR API documentation
- European MAR systems (UK, Germany, France, etc.)
- Polish KNF/ESPI system
- Form 4 structure and XML parsing
- Key data points and thresholds
- Free APIs and commercial alternatives
- Rate limits and best practices
- Legal & compliance notes

**Best for:** Deep diving into insider trading data sources

#### 2. **INSIDER_TRADING_README.md** (1,000+ lines)
**User manual with:**
- Installation instructions
- Quick start guide
- Output examples
- Signal explanation
- Configuration guide
- Integration examples
- Troubleshooting tips
- Best practices

**Best for:** Learning how to use the fetcher tool

#### 3. **INSIDER_TRADING_SUMMARY.md**
**Project summary including:**
- Quick reference for all markets
- File descriptions
- Key data points tracked
- Signal system explanation
- Transaction codes
- Free APIs list
- Code examples
- Integration strategies

**Best for:** Understanding the complete package

#### 4. **INSIDER_TRADING_QUICK_REFERENCE.md**
**Quick lookup guide with:**
- One-line commands
- Quick Python examples
- Key URLs
- Signal quick guide
- Transaction codes
- Common filters
- Troubleshooting

**Best for:** Quick reference while coding

#### 5. **This File - INSIDER_TRADING_INDEX.md**
**Package overview and navigation**

---

### 💻 Code Files (3 files)

#### 6. **insider_trading_fetcher.py** (600+ lines)
**Production-ready Python tool**

**Features:**
- `SECInsiderTrading` class for data fetching
- `InsiderSignalAnalyzer` class for signal generation
- Command-line interface
- Batch processing
- CSV export
- Configurable rate limiting

**Usage:**
```bash
# Basic
python insider_trading_fetcher.py --ticker AAPL

# With details and signals
python insider_trading_fetcher.py --ticker AAPL --details --signals

# Multiple tickers
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals

# Export to CSV
python insider_trading_fetcher.py --ticker AAPL --details --signals --output trades.csv
```

**Classes:**
- `SECInsiderTrading` - Main fetcher class
  - `load_ticker_mappings()` - Load ticker to CIK mappings
  - `get_cik(ticker)` - Convert ticker to CIK
  - `get_form4_filings(ticker, days_back)` - Get filings
  - `get_insider_trading(ticker, days_back, fetch_details)` - Main method
  - `get_multiple_tickers(tickers, days_back, fetch_details)` - Batch processing
  - `parse_form4(filing_text)` - Parse XML

- `InsiderSignalAnalyzer` - Signal generation
  - `calculate_signal(transaction)` - Calculate signal for one transaction
  - `analyze_dataframe(df)` - Add signals to DataFrame

#### 7. **example_insider_trading.py** (300+ lines)
**Seven practical examples:**

1. `example_1_basic_fetch()` - Basic fetch for single ticker
2. `example_2_detailed_transactions()` - Detailed transaction data
3. `example_3_signal_analysis()` - Generate trading signals
4. `example_4_multiple_tickers()` - Batch process multiple stocks
5. `example_5_find_best_opportunities()` - Find strongest insider buying
6. `example_6_export_to_csv()` - Export data to CSV
7. `example_7_filter_executive_trades()` - Filter C-level trades

**Usage:**
```bash
python example_insider_trading.py
```

#### 8. **backend/routes/insider-trading.js**
**Express.js route for web API integration**

**Features:**
- REST API endpoint for insider trading data
- Integrates with existing backend
- Returns JSON responses

**Endpoint:**
```
GET /api/insider-trading?ticker=AAPL&days=30
```

---

### ⚙️ Configuration Files (2 files)

#### 9. **requirements-insider-trading.txt**
**Python dependencies**

**Contents:**
```
requests>=2.31.0
pandas>=2.0.0
psycopg2-binary>=2.9.0  # Optional: PostgreSQL
python-telegram-bot>=20.0  # Optional: Telegram alerts
```

**Install:**
```bash
pip install -r requirements-insider-trading.txt
```

#### 10. **insider_trading_config.example.json**
**Configuration template**

**Sections:**
- SEC EDGAR settings
- Telegram notifications
- Database configuration
- Monitoring watchlist
- Signal thresholds
- Filters
- Logging

**Usage:**
```bash
cp insider_trading_config.example.json insider_trading_config.json
# Edit with your settings
```

---

## File Navigation Guide

### For Beginners

1. **Start here:** `INSIDER_TRADING_QUICK_REFERENCE.md`
2. **Then read:** `INSIDER_TRADING_README.md`
3. **Run examples:** `python example_insider_trading.py`
4. **Try it yourself:** `python insider_trading_fetcher.py --ticker AAPL --details --signals`

### For Advanced Users

1. **Deep dive:** `insider-trading-data-guide.md`
2. **Integrate:** Use `insider_trading_fetcher.py` classes
3. **Reference:** `INSIDER_TRADING_SUMMARY.md`
4. **API docs:** Check docstrings in Python files

### For Integration with Oneshot FTMO

1. **Review:** `INSIDER_TRADING_SUMMARY.md` - Integration section
2. **Use:** `insider_trading_fetcher.py` - Import classes
3. **Example:** See `example_insider_trading.py` - Example 7
4. **Configure:** `insider_trading_config.example.json`

---

## Key Concepts

### Signal System

The tool generates 5 signal levels based on:
- Transaction type (buy/sell)
- Transaction size (value)
- Insider position (CEO/CFO vs Director)
- Ownership percentage change

**Signals:**
- 🚀🚀🚀 **STRONG_BUY** - CEO/CFO bought >$1M
- 🚀 **BUY** - Executive bought >$100k
- ➡️ **NEUTRAL** - Mixed or small trades
- ⚠️ **SELL** - Executive selling
- 🔴🔴🔴 **STRONG_SELL** - CEO sold large %

### Transaction Codes

- **P** - Purchase (Bullish)
- **S** - Sale (Bearish)
- **A** - Award/Grant (Neutral-Bullish)
- **X** - Option Exercise (Neutral)

### Data Flow

```
1. User Input (Ticker, Days)
   ↓
2. Fetch SEC Company Tickers JSON
   ↓
3. Get Company Submissions (Form 4 list)
   ↓
4. Download Form 4 Filing Text
   ↓
5. Parse XML for Transactions
   ↓
6. Calculate Signals
   ↓
7. Display / Export Results
```

---

## Integration Examples

### Example 1: Pre-Trade Filter

```python
from insider_trading_fetcher import SECInsiderTrading, InsiderSignalAnalyzer

def check_insider_sentiment(ticker, days_back=7):
    sec = SECInsiderTrading()
    df = sec.get_insider_trading(ticker, days_back, fetch_details=True)

    if df.empty:
        return True  # No data, skip filter

    df = InsiderSignalAnalyzer.analyze_dataframe(df)

    # Only allow trades if recent insider buying
    recent_buys = df[
        df['transaction_code'] == 'P'
    ]['signal'].isin(['BUY', 'STRONG_BUY']).any()

    return recent_buys

# Usage in trading system
if check_insider_sentiment('XAUUSD'):
    # Allow LONG trade
    pass
```

### Example 2: Stock Selection

```python
def find_best_insider_stocks(tickers, days_back=30):
    sec = SECInsiderTrading()
    results = []

    for ticker in tickers:
        df = sec.get_insider_trading(ticker, days_back, fetch_details=True)
        if not df.empty:
            df = InsiderSignalAnalyzer.analyze_dataframe(df)

            strong_buys = df[df['signal'] == 'STRONG_BUY']
            if len(strong_buys) > 0:
                total_value = df[df['signal'].isin(['BUY', 'STRONG_BUY'])]['total_value'].sum()
                results.append({'ticker': ticker, 'value': total_value})

    return sorted(results, key=lambda x: x['value'], reverse=True)

# Usage
tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA']
best = find_best_insider_stocks(tickers)
print(f"Top stock: {best[0]['ticker']} (${best[0]['value']:,.0f})")
```

### Example 3: Telegram Alerts

```python
import requests

def send_insider_alert(transaction):
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"

    emoji = {
        'STRONG_BUY': '🚀🚀🚀',
        'BUY': '🚀',
        'SELL': '⚠️'
    }

    message = f"""
🔔 <b>Insider Alert</b>

{emoji.get(transaction['signal'], '📊')} {transaction['signal']}

<b>{transaction['ticker']}</b>
{transaction['insider_name']} ({transaction['position']})
{transaction['transaction_type']}: {transaction['shares']:,.0f} shares
Value: ${transaction['total_value']:,.2f}
"""

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    })

# Usage
for _, row in df.iterrows():
    if row['signal'] in ['STRONG_BUY', 'BUY']:
        send_insider_alert(row.to_dict())
```

---

## Data Sources Covered

### ✅ US Market (SEC)
- SEC EDGAR API (FREE)
- OpenInsider.com
- Finviz
- InsiderMonkey
- SECForm4.com

### ✅ European Market
- UK: FCA National Storage Mechanism
- Germany: BaFin Directors' Dealings
- France: AMF disclosures
- Other EU countries (Netherlands, Italy, Spain, etc.)

### ✅ Polish Market
- KNF ESPI system
- Bankier.pl
- Stooq.pl
- GPW (Warsaw Stock Exchange)

---

## Important Thresholds

| Region | Minimum Transaction | Reporting Deadline |
|--------|-------------------|-------------------|
| **US (SEC)** | $10,000 | 2 business days |
| **EU (MAR)** | €5,000 | 3 business days |
| **Poland (KNF)** | PLN 20,000 | 3 business days |

---

## Rate Limits

### SEC EDGAR
- **Official limit:** 10 requests/second
- **Tool default:** 5 requests/second (safe)
- **Requirement:** User-Agent header

### Best Practices
✅ Always include User-Agent
✅ Implement rate limiting
✅ Use caching
✅ Handle errors gracefully
✅ Batch efficiently

---

## Legal & Compliance

✅ **Legal to Use** - SEC Form 4 data is public information
✅ **Not Insider Trading** - Using public filings is legal
⚠️ **Verify Data** - Errors can occur in filings
⚠️ **Respect Limits** - Essential for continued access
⚠️ **Cite Sources** - When distributing data

---

## Installation

```bash
# 1. Navigate to directory
cd /Users/maciejmostowski/trading-webhook-stack

# 2. Install dependencies
pip install -r requirements-insider-trading.txt

# 3. Run example
python example_insider_trading.py

# 4. Try it yourself
python insider_trading_fetcher.py --ticker AAPL --details --signals
```

---

## Quick Commands Reference

```bash
# Single ticker, basic
python insider_trading_fetcher.py --ticker AAPL

# Single ticker, detailed with signals
python insider_trading_fetcher.py --ticker AAPL --details --signals

# Multiple tickers
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals

# Export to CSV
python insider_trading_fetcher.py --ticker AAPL --details --signals --output trades.csv

# Custom date range (60 days)
python insider_trading_fetcher.py --ticker AAPL --details --signals --days 60

# Custom User-Agent
python insider_trading_fetcher.py --ticker AAPL --user-agent "Your Name (email@example.com)"

# Run all examples
python example_insider_trading.py
```

---

## Support & Resources

### Documentation
- **Quick Start:** `INSIDER_TRADING_QUICK_REFERENCE.md`
- **User Guide:** `INSIDER_TRADING_README.md`
- **Complete Reference:** `insider-trading-data-guide.md`
- **Project Summary:** `INSIDER_TRADING_SUMMARY.md`

### Official Resources
- **SEC EDGAR API:** https://www.sec.gov/edgar/sec-api-documentation
- **Form 4 Instructions:** https://www.sec.gov/files/form4-instructions.pdf
- **MAR Guidelines:** https://www.esma.europa.eu/market-abuse-regulation-mar

### Tools & Libraries
- **Python:** requests, pandas, sqlalchemy
- **Node.js:** axios, cheerio
- **Database:** PostgreSQL, MongoDB

---

## Version History

**v1.0 (2026-02-06)**
- Initial release
- SEC EDGAR integration
- Form 4 parsing
- Signal generation
- Batch processing
- CSV export
- Comprehensive documentation
- Examples and integration guides

---

## Checklist

### Getting Started
- [ ] Read `INSIDER_TRADING_QUICK_REFERENCE.md`
- [ ] Install dependencies: `pip install -r requirements-insider-trading.txt`
- [ ] Run example: `python example_insider_trading.py`
- [ ] Test with single ticker: `python insider_trading_fetcher.py --ticker AAPL --details --signals`
- [ ] Review output and signals

### Integration
- [ ] Review integration examples in `INSIDER_TRADING_SUMMARY.md`
- [ ] Copy `insider_trading_config.example.json` to your config
- [ ] Test with your watchlist tickers
- [ ] Set up Telegram alerts (optional)
- [ ] Add to your trading system filter

### Production
- [ ] Set up daily monitoring (cron/task scheduler)
- [ ] Configure database storage (optional)
- [ ] Test rate limiting
- [ ] Monitor SEC API changes
- [ ] Review and optimize queries

---

## Summary

This package provides everything you need to fetch, analyze, and utilize insider trading data:

✅ **10 files** including documentation, code, and configuration
✅ **14,000+ words** of comprehensive documentation
✅ **Production-ready** Python tool with 600+ lines
✅ **7 practical examples** demonstrating all features
✅ **Free SEC API** integration (no API key required)
✅ **Signal generation** with 5 levels
✅ **Ready for integration** with Oneshot FTMO system

**All files located in:** `/Users/maciejmostowski/trading-webhook-stack/`

---

**Remember:** Insider trading data is just one factor. Always combine with other analysis methods and proper risk management.

**End of Index**

For detailed information, refer to individual documentation files.
