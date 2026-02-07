# Insider Trading Data Sources - Complete Summary

## Overview

This document provides a comprehensive guide to insider trading data sources across US, European, and Polish markets, including free APIs, code examples, and integration strategies.

## Quick Reference

### US Market (SEC)
- **API**: SEC EDGAR (FREE)
- **Endpoint**: `https://www.sec.gov/Archives/edgar/data/`
- **Rate Limit**: 10 requests/second
- **Coverage**: All US public companies
- **Format**: XML/JSON
- **Documentation**: See `insider-trading-data-guide.md`

### European Market (MAR)
- **UK**: FCA National Storage Mechanism
- **Germany**: BaFin Directors' Dealings
- **France**: AMF disclosures (PDF)
- **Other**: Country-specific regulators

### Polish Market (KNF)
- **System**: ESPI (Electronic System for Transmission of Information)
- **URL**: https://www.knf.gov.pl/
- **Language**: Polish/English
- **Format**: PDF reports

## Files Created

### 1. `insider-trading-data-guide.md` (14,000+ words)
**Complete reference guide covering:**
- US SEC EDGAR API documentation
- Form 4 structure and parsing
- European MAR systems by country
- Polish KNF/ESPI system
- Key data points to track
- Important thresholds (US, EU, Poland)
- Free APIs and data sources
- Rate limits and best practices
- Commercial alternatives

### 2. `insider_trading_fetcher.py` (600+ lines)
**Production-ready Python tool:**
```bash
# Basic usage
python insider_trading_fetcher.py --ticker AAPL

# With details and signals
python insider_trading_fetcher.py --ticker AAPL --details --signals

# Multiple stocks
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals

# Export to CSV
python insider_trading_fetcher.py --ticker AAPL --details --output aapl.csv
```

**Features:**
- Fetch SEC Form 4 filings
- Parse XML transaction data
- Generate trading signals
- Batch processing
- CSV export
- Configurable rate limiting

### 3. `INSIDER_TRADING_README.md` (1,000+ lines)
**User documentation with:**
- Installation instructions
- Quick start guide
- Output examples
- Signal explanation
- Configuration guide
- Integration examples
- Troubleshooting tips
- Best practices

### 4. `example_insider_trading.py` (300+ lines)
**Seven practical examples:**
1. Basic fetch for single ticker
2. Detailed transaction data
3. Signal analysis
4. Multiple tickers batch processing
5. Find best opportunities
6. Export to CSV
7. Filter C-level executive trades

### 5. `requirements-insider-trading.txt`
**Python dependencies:**
```
requests>=2.31.0
pandas>=2.0.0
psycopg2-binary>=2.9.0  # Optional: PostgreSQL
python-telegram-bot>=20.0  # Optional: Telegram alerts
```

### 6. `insider_trading_config.example.json`
**Configuration template:**
```json
{
  "sec_edgar": {
    "user_agent": "Your Name (your.email@example.com)",
    "rate_limit_per_second": 5
  },
  "telegram": {
    "enabled": false,
    "bot_token": "YOUR_BOT_TOKEN"
  },
  "monitoring": {
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "check_interval_hours": 24
  }
}
```

## Key Data Points Tracked

### Insider Information
- Full name
- Position (CEO, CFO, Director, etc.)
- Relationship (Officer, Director, 10% owner)

### Transaction Details
- Transaction type (Buy/Sell/Grant/Exercise)
- Price per share
- Number of shares
- Total value
- Transaction date
- Filing date

### Ownership Information
- Shares owned before
- Shares owned after
- Ownership percentage change

### Important Thresholds

| Region | Minimum | Reporting Deadline | Major Shareholder |
|--------|---------|-------------------|-------------------|
| **US (SEC)** | $10,000 | 2 business days | 5% / 10% |
| **EU (MAR)** | €5,000 | 3 business days | 20% |
| **Poland (KNF)** | PLN 20,000 | 3 business days | - |

## Signal System

### Signal Levels

🚀🚀🚀 **STRONG_BUY**
- Score ≥ 5
- Large purchase by CEO/CFO
- >$1M transaction value
- Significant ownership increase

🚀 **BUY**
- Score ≥ 3
- Purchase by executive/director
- >$100k transaction value
- Moderate ownership increase

➡️ **NEUTRAL**
- Score ≥ 0
- Small transactions
- Awards/grants
- Mixed signals

⚠️ **SELL**
- Score ≥ -2
- Sales by executives
- Large percentage sales

🔴🔴🔴 **STRONG_SELL**
- Score < -2
- Large CEO/CFO sales
- Significant ownership decrease

### Transaction Codes

| Code | Description | Sentiment |
|------|-------------|-----------|
| P | Open market purchase | Bullish +2 |
| S | Open market sale | Bearish -1 |
| A | Grant/Award | Neutral +1 |
| X | Option exercise | Neutral |
| M | Multiple transactions | Neutral |

## Free APIs & Data Sources

### Completely Free

1. **SEC EDGAR API** ⭐⭐⭐⭐⭐
   - URL: https://www.sec.gov/Archives/edgar/data/
   - Rate Limit: 10 requests/second
   - Coverage: All US public companies
   - Format: XML/JSON
   - Auth: User-Agent required

2. **OpenInsider** ⭐⭐⭐⭐
   - URL: https://openinsider.com/
   - Features: Real-time data, RSS feeds
   - Limit: No official API

3. **Finviz** ⭐⭐⭐⭐
   - URL: https://finviz.com/insidertrading.ashx
   - Features: Free with registration
   - Format: HTML tables

### Freemium

4. **Financial Modeling Prep**
   - Free: 250 requests/day
   - Insider endpoint available

5. **InsiderMonkey**
   - Free articles with limited data
   - Premium for full access

## Code Examples

### Quick Start

```python
from insider_trading_fetcher import SECInsiderTrading, InsiderSignalAnalyzer

# Initialize
sec = SECInsiderTrading()

# Fetch data
df = sec.get_insider_trading('AAPL', days_back=30, fetch_details=True)

# Generate signals
df = InsiderSignalAnalyzer.analyze_dataframe(df)

# Show strong buys
strong_buys = df[df['signal'] == 'STRONG_BUY']
print(strong_buys[['insider_name', 'shares', 'total_value']])
```

### Integration with Oneshot FTMO

```python
# In your Oneshot_FTMO.mq5 or Oneshot_AutoTrader.cs

# Example: Add insider sentiment filter
def CheckInsiderSentiment(ticker, days_back=7):
    sec = SECInsiderTrading()
    df = sec.get_insider_trading(ticker, days_back, fetch_details=True)

    if df.empty:
        return False  # No data, skip filter

    df = InsiderSignalAnalyzer.analyze_dataframe(df)

    # Only trade if recent insider buying
    recent_buys = df[
        df['transaction_code'] == 'P'
    ]['signal'].isin(['BUY', 'STRONG_BUY']).any()

    return recent_buys

# Usage in trading system
if CheckInsiderSentiment('XAUUSD'):
    # Allow trade
else:
    # Skip trade
```

## Rate Limits & Best Practices

### SEC EDGAR

**Official Limits:**
- 10 requests per second per IP
- User-Agent header mandatory
- Blocks excessive requests

**Recommended:**
- Use 5 requests per second (tool default)
- Always include User-Agent
- Implement caching
- Handle errors gracefully
- Use batch processing

### Best Practices

1. **Always identify yourself:**
   ```python
   headers = {'User-Agent': 'Your Name (your.email@example.com)'}
   ```

2. **Implement rate limiting:**
   ```python
   time.sleep(0.2)  # 5 requests per second
   ```

3. **Use caching:**
   ```python
   @functools.lru_cache(maxsize=1000)
   def cached_get_cik(ticker):
       # ...
   ```

4. **Batch efficiently:**
   ```python
   for i in range(0, len(items), batch_size):
       # Process batch
       time.sleep(delay)
   ```

## Integration Strategies

### 1. As Additional Filter

Only take trades when insiders are buying:

```python
if CheckInsiderSentiment(ticker):
    # Proceed with trade
else:
    # Skip trade
```

### 2. For Stock Selection

Focus on stocks with strongest insider buying:

```python
# Rank stocks by insider buying
ranked = rank_by_insider_buying(tickers)
# Trade top 3
```

### 3. For Position Sizing

Increase size when multiple insiders buy:

```python
if count_insider_buys(ticker) > 2:
    position_size *= 1.5
```

### 4. For Sentiment Analysis

Combine with ATF signals:

```python
if atf_signal == 'BULLISH' and insider_signal == 'BUY':
    confidence = 'HIGH'
```

## Installation

```bash
# Clone or navigate to directory
cd trading-webhook-stack

# Install dependencies
pip install -r requirements-insider-trading.txt

# Run example
python example_insider_trading.py

# Run fetcher
python insider_trading_fetcher.py --ticker AAPL --details --signals
```

## Troubleshooting

### Common Issues

**"Ticker not found"**
- Check ticker symbol
- Ensure it's a US public company
- Run without --details first

**"No Form 4 filings found"**
- Normal for low insider activity
- Try increasing --days
- Verify company has reporting insiders

**"Error downloading Form 4"**
- Network issue
- SEC temporarily unavailable
- Wait and retry

**Rate limiting**
- Reduce batch size
- Increase delay
- Cache locally

## Legal & Compliance

✅ **Legal to Use**
- SEC Form 4 data is public information
- No restrictions on using public filings

✅ **Not Insider Trading**
- Using public disclosures is legal
- Not the same as illegal insider trading

⚠️ **Verify Data**
- Errors can occur in filings
- Cross-check important data

⚠️ **Respect Limits**
- Essential for continued access
- Follow SEC rate limits

⚠️ **Cite Sources**
- When distributing data
- Credit SEC EDGAR

## Data Quality

### Green Flags (Bullish)
✅ Multiple insiders buying simultaneously
✅ CEO/CFO buys significant amount
✅ Buys at market price (not options)
✅ New positions initiated
✅ Buys after price drops

### Red Flags (Bearish)
⚠️ Multiple insiders selling
⚠️ CEO sells large % of holdings
⚠️ Timed sales (10b5-1 plans) - less significant
⚠️ Option exercises + sell all - neutral

### Neutral/Common
- Option exercises (automatic)
- 10b5-1 planned sales (pre-arranged)
- Small percentage trades (<1%)
- Tax-related sales

## Additional Resources

### Official Documentation
- [SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)
- [Form 4 Instructions](https://www.sec.gov/files/form4-instructions.pdf)
- [MAR Guidelines](https://www.esma.europa.eu/market-abuse-regulation-mar)

### Tools & Libraries
- Python: requests, pandas, sqlalchemy
- Node.js: axios, cheerio
- Database: PostgreSQL, MongoDB

### Communities
- Reddit: r/algotrading, r/stocks
- Discord: Trading servers
- GitHub: Open source trading bots

## Version History

**v1.0 (2026-02-06)**
- Initial release
- SEC EDGAR integration
- Form 4 parsing
- Signal generation
- Batch processing
- CSV export
- Comprehensive documentation

## Support

For issues or questions:
1. Review documentation in `insider-trading-data-guide.md`
2. Check `INSIDER_TRADING_README.md` for usage examples
3. Run `example_insider_trading.py` to see examples
4. Verify network connectivity and rate limits

---

**Important:** Insider trading data is just one factor. Always combine with other analysis methods and proper risk management. Past insider activity does not guarantee future results.

## Quick Start Commands

```bash
# 1. Install dependencies
pip install requests pandas

# 2. Run example
python example_insider_trading.py

# 3. Fetch single ticker
python insider_trading_fetcher.py --ticker AAPL --details --signals

# 4. Fetch multiple tickers
python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL --details --signals

# 5. Export to CSV
python insider_trading_fetcher.py --ticker AAPL --details --signals --output trades.csv

# 6. Find best opportunities
python example_insider_trading.py | grep "Top Insider"
```

## File Locations

All files created in: `/Users/maciejmostowski/trading-webhook-stack/`

1. `insider-trading-data-guide.md` - Complete reference guide
2. `insider_trading_fetcher.py` - Main fetcher tool
3. `INSIDER_TRADING_README.md` - User documentation
4. `example_insider_trading.py` - Usage examples
5. `requirements-insider-trading.txt` - Dependencies
6. `insider_trading_config.example.json` - Configuration template
7. `INSIDER_TRADING_SUMMARY.md` - This file

---

**End of Summary**

For detailed information, refer to the individual documentation files.
