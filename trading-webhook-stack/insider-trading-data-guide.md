# Insider Trading Data Sources & APIs - Comprehensive Guide

*Last Updated: February 2026*

## Table of Contents
1. [US Market (SEC)](#us-market-sec)
2. [European Market](#european-market)
3. [Polish Market (KNF)](#polish-market-knf)
4. [Key Data Points to Track](#key-data-points-to-track)
5. [Free APIs and Data Sources](#free-apis-and-data-sources)
6. [Code Examples](#code-examples)
7. [Rate Limits & Best Practices](#rate-limits--best-practices)

---

## US Market (SEC)

### SEC EDGAR API

**Base URL:** `https://www.sec.gov/Archives/edgar/data/`

#### Key Endpoints

**1. Company Search (CIK Lookup)**
```
GET https://www.sec.gov/files/company_tickers.json
```
Returns: JSON mapping of tickers to CIK (Central Index Key) numbers

**2. Form 4 Filings (Insider Trading)**
```
GET https://www.sec.gov/Archives/edgar/data/{CIK}/0000320193-000001.txt
```
- `{CIK}`: Company's Central Index Key (10 digits, zero-padded)
- Returns: Full filing submission text file

**3. Form 4 Search by Date**
```
GET https://www.sec.gov/Archives/edgar/daily-index/{YEAR}/{QTR}/company.{YYYYMMDD}.idx
```
- `{YEAR}`: 4-digit year
- `{QTR}`: Quarter (QTR1, QTR2, QTR3, QTR4)
- Returns: Daily index of all filings

**4. Submissions List**
```
GET https://data.sec.gov/submissions/CIK{CIK}.json
```
- Returns: JSON with recent filings including Form 4

#### Important Headers
```http
User-Agent: Your Name (your.email@example.com)
Accept-Encoding: gzip, deflate
Accept: application/json
```

**Note:** SEC requires User-Agent identification. Requests without proper User-Agent may be blocked.

#### Form 4 XML Structure
Form 4 filings contain XML documents with this structure:
- `ownershipDocument` - Root element
- `subjectCompany` - Company information
- `reportingOwner` - Insider details (name, position)
- `derivativeTable` - Derivative securities
- `nonDerivativeTable` - Non-derivative securities (common stock)
  - `transactionAmounts` - Price, quantity, transaction type
  - `postTransactionAmounts` - Holdings after transaction

#### CIK Examples
- Apple: `0000320193`
- Microsoft: `0000789019`
- Tesla: `0001318605`
- Amazon: `0001018724`
- Google: `0001652044`

---

### Insider Tracking Websites (US)

#### 1. OpenInsider
**URL:** https://openinsider.com/

**Features:**
- Real-time insider trading data
- Searchable by ticker, insider name, date range
- Export to CSV
- Free RSS feeds

**Data Points:**
- Insider name, position
- Transaction type (buy/sell, option exercise)
- Price, volume, total value
- Filing date
- % of holdings traded

**API Status:** No official API, but data can be scraped (respect robots.txt)

**Premium Features:**
- Advanced screening tools
- Email alerts
- Historical data downloads

#### 2. InsiderMonkey
**URL:** https://insidermonkey.com/

**Features:**
- Insider trading news and analysis
- Hedge fund holdings tracking
- Insider sentiment scores
- Top insider purchases/sales lists

**Data Access:**
- Free articles with limited data
- Premium subscription for full access

#### 3. WhaleRock
**URL:** https://whalerock.xyz/

**Features:**
- Modern, clean interface
- Real-time insider alerts
- Portfolio tracking
- Dark pool data

**Pricing:** Freemium model

#### 4. SEC Form 4 Scanner
**URL:** https://www.secform4.com/

**Features:**
- Simple Form 4 search
- Email alerts
- Excel export
- Free and premium tiers

#### 5. Finviz
**URL:** https://finviz.com/

**Insider Section:** https://finviz.com/insidertrading.ashx

**Features:**
- Latest insider trades
- Filter by market cap, sector, transaction type
- Shows ownership percentage
- Free with registration

---

## European Market

### MAR (Market Abuse Regulation) Overview

Since July 2016, EU insiders must report trades to their national regulator within 3 business days. Data is then published publicly.

### Country-Specific Systems

#### 1. United Kingdom (FCA)

**FCA Disclosure Transparency Rules**
**URL:** https://www.fca.org.uk/

**Data Source:**
- **National Storage Mechanism (NSM)**
- URL: https://www.disclosures.org.uk/
- Operated by TR-1 (part of London Stock Exchange Group)

**API Access:**
```
GET https://www.disclosures.org.uk/api/transactions
```

**Data Format:** JSON/XML

**Key Fields:**
- Person discharging managerial responsibilities (PDMR)
- Issuer name and ticker
- Transaction details (price, volume, date)
- Venue of transaction
- Notification date

#### 2. Germany (BaFin)

**BaFin Database**
**URL:** https://www.bafin.de/

**Directors' Dealings:** https://www.bafin.de/DE/Anleger/Dienstleistungen/Datenbanken/db_directors_dealings_node.html

**Features:**
- Search by company or insider name
- Download as CSV/Excel
- German interface (English available)

**Data Points:**
- Insider name, position
- Company name, ISIN
- Transaction type, volume, price
- Date of trade and notification

**API:** No official API, web scraping possible (respect rate limits)

#### 3. France (AMF)

**AMF Sanctions & Notifications**
**URL:** https://www.amf-france.org/

**Insider Trading Disclosures:** https://www.amf-france.org/Epargne-Info/Documentation-publique/Transactions-sur-instruments-financiers

**Access:** Online database search, PDF downloads

**Data Format:** Mostly PDF documents (parsing required)

#### 4. Other EU Countries

| Country | Regulator | Website | Data Access |
|---------|-----------|---------|-------------|
| **Netherlands** | AFM | https://www.afm.nl/ | Online database |
| **Italy** | CONSOB | https://www.consob.it/ | PDF notifications |
| **Spain** | CNMV | https://www.cnmv.es/ | Online database |
| **Sweden** | FI | https://www.fi.se/ | Online search |
| **Switzerland** | FINMA | https://www.finma.ch/ | SIX exchange data |
| **Belgium** | FSMA | https://www.fsma.be/ | Online database |
| **Austria** | FMA | https://www.fma.gv.at/ | Online database |

### Pan-European Sources

#### 1. Morningstar
**URL:** https://www.morningstar.co.uk/

**Insider Trading:** https://www.morningstar.co.uk/uk/marketinsider

**Features:**
- Coverage of major European stocks
- Insider sentiment scores
- Historical data (premium)

#### 2. Markit Insider Research
**URL:** https://www.markit.com/

**Professional Platform:** Paid subscription, comprehensive EU coverage

---

## Polish Market (KNF)

### Komisja Nadzoru Finansowego (KNF)

**Official Website:** https://www.knf.gov.pl/

### Insider Trading Disclosure System

**Current System:** ESPI (Electronic System for Transmission of Information)

**URL:** https://www.knf.gov.pl/en/menu/5/information-disp-layed-in-espi

**Language:** Polish/English interface available

#### Access Methods

**1. ESPI Database Search**
**URL:** https://www.knf.gov.pl/en/menu/5/information-disp-layed-in-espi

**Features:**
- Search by company name (spółka)
- Search by date range
- Filter by report type (current, periodic)
- Download PDF reports

**2. Direct Company Disclosures**

Polish listed companies must report insider trades to ESPI within 3 business days.

**Report Types:**
- **RAP** (Raport bieżący) - Current report
- **RB RBI** - Insider trading notification
- Specific codes: RB RBI, RB RBP, RB RBO

#### Data Points in Polish Filings

**Key Information:**
- **Spółka** (Company) - Name and ticker (e.g., KGHM, PKN Orlen)
- **Osoba zobowiązana** (Obligating person) - Insider name
- **Data transakcji** (Transaction date)
- **Rodzaj transakcji** (Transaction type) - Zakup (buy), Sprzedaż (sell)
- **Cena** (Price) - PLN per share
- **Liczba akcji** (Number of shares)
- **Wartość transakcji** (Transaction value) - Total PLN
- **Udział** (Ownership percentage) - Before and after

#### Example Polish Companies

| Company | Ticker | Exchange |
|---------|--------|----------|
| KGHM Polska Miedź | KGH | GPW |
| PKN Orlen | PKN | GPW |
| PZU | PZU | GPW |
| PKO BP | PKO | GPW |
| Dino Polska | DNP | GPW |
| CD Projekt | CDR | GPW |
| Allegro | ALE | GPW |
| LPP | LPP | GPW |

#### Alternative Polish Sources

**1. Bankier.pl**
**URL:** https://www.bankier.pl/

**Insider Section:** https://www.bankier.pl/gielda/notyfikacje

**Features:**
- Aggregated insider trading data
- Search by company
- Historical data
- Free access

**2. Stooq.pl
**URL:** https://stooq.pl/

**Features:**
- Market data including insider filings
- API available for some data

**3. GPW (Warsaw Stock Exchange)**
**URL:** https://www.gpw.pl/

**Data:** Official exchange data, some insider information

#### KNF ESPI API

**Status:** No official public API

**Workaround:**
1. Monitor KNF RSS feeds
2. Parse HTML from ESPI website
3. Use commercial data providers

---

## Key Data Points to Track

### Essential Data Points

#### 1. Insider Information
- **Full Name** - First and last name
- **Position/Title** - CEO, CFO, COO, Director, 10% owner, etc.
- **Relationship** - Officer, Director, Beneficial Owner (5%, 10%)

#### 2. Company Information
- **Company Name** - Legal entity name
- **Ticker Symbol** - Stock exchange symbol
- **CIK/ISIN** - Unique identifier
- **Exchange** - NYSE, NASDAQ, GPW, etc.

#### 3. Transaction Details
- **Transaction Type**
  - `P` - Purchase (Open market or private)
  - `S` - Sale (Open market or private)
  - `M` - Multiple transactions
  - `A` - Grant/Award (Option award, restricted stock)
  - `D` - Sale to issuer
  - `F` - Payment of exercise price
  - `G` - Gift
  - Other codes available

- **Transaction Date** - When trade occurred
- **Filing Date** - When report filed (should be within 2-3 business days)
- **Price Per Share** - Execution price
- **Shares Traded** - Number of shares
- **Total Value** - Price × Shares

#### 4. Ownership Information
- **Shares Owned Before Transaction** - Total holdings prior
- **Shares Owned After Transaction** - Total holdings after
- **% Ownership Change** - Change in percentage stake
- **Direct/Indirect** - Ownership type

#### 5. Important Thresholds

**US SEC:**
- **$10,000** - Minimum transaction value for Form 4
- **$5,000,000** - Large transactions requiring accelerated filing
- **5%** - Beneficial ownership threshold (Schedule 13D)
- **10%** - Major shareholder threshold

**European MAR:**
- **€5,000** - Minimum reporting threshold
- **3 business days** - Reporting deadline
- **20%** - Major shareholder threshold

**Polish KNF:**
- **PLN 20,000** - Minimum threshold for reporting
- **3 business days** - Reporting deadline (ESPI)

### Data Quality Indicators

#### Green Flags (Bullish Signals)
✅ Multiple insiders buying simultaneously
✅ CEO/CEO buys significant amount
✅ Buys at market price (not options)
✅ New position initiated
✅ Buys after price drop
✅ Historical success rate of insider

#### Red Flags (Bearish Signals)
⚠️ Multiple insiders selling
⚠️ CEO sells large % of holdings
⚠️ Timed sales (10b5-1 plans) - less significant
⚠️ Option exercises + sell all - neutral/standard
⚠️ Sales near all-time highs

#### Neutral/Common Transactions
- Option exercises (automatic)
- 10b5-1 planned sales (pre-arranged)
- Small percentage trades (<1% of holdings)
- Tax-related sales

---

## Free APIs and Data Sources

### Completely Free Sources

#### 1. SEC EDGAR API
**Cost:** FREE
**Rate Limit:** 10 requests/second
**Auth Required:** No (but need User-Agent header)
**Data Quality:** ⭐⭐⭐⭐⭐ (Official source)

**Coverage:**
- All US public companies
- Real-time filings
- Historical data back to 1990s
- Complete Form 4 data

**Pros:**
- Official, accurate data
- No API key required
- Comprehensive coverage
- Free forever

**Cons:**
- Raw XML/JSON format (parsing required)
- Rate limiting enforced
- No aggregated insights
- Technical documentation required

**Best For:** Building custom applications, research

#### 2. SEC Company Tickers JSON
**URL:** https://www.sec.gov/files/company_tickers.json

**Updates:** Daily
**Format:** JSON
**Size:** ~10MB

**Usage:**
```python
import requests
import pandas as pd

# Fetch ticker to CIK mapping
response = requests.get('https://www.sec.gov/files/company_tickers.json')
data = response.json()

# Convert to DataFrame
df = pd.DataFrame.from_dict(data.values())
df.columns = ['CIK', 'Ticker', 'Company Name']

# Zero-pad CIK to 10 digits
df['CIK'] = df['CIK'].astype(str).str.zfill(10)

print(df.head())
```

#### 3. OpenInsider (Free Tier)
**Cost:** FREE
**Rate Limit:** None specified
**Auth Required:** No
**Data Quality:** ⭐⭐⭐⭐

**Coverage:**
- All US insider trades
- Real-time updates
- Historical data (limited on free tier)

**Free Features:**
- Search by ticker
- Latest trades
- RSS feeds
- CSV export (limited)

**Paid Features:**
- Advanced screening
- Email alerts
- Full historical download
- API access

**Best For:** Quick lookups, monitoring specific stocks

#### 4. Finviz Insider Trading
**Cost:** FREE
**Rate Limit:** None (registration required)
**Auth Required:** Free account
**Data Quality:** ⭐⭐⭐⭐

**URL:** https://finviz.com/insidertrading.ashx

**Free Features:**
- Latest insider trades
- Filter by market cap, sector
- Shows ownership %
- Excel-friendly format

**Best For:** Daily scanning, quick overview

#### 5. IEX Cloud (Free Tier)
**Cost:** FREE (100k calls/month)
**Auth Required:** API token
**Data Quality:** ⭐⭐⭐

**Insider Endpoint:** Not available on free tier (paid only)

**Alternative:** Use for stock prices, company info

#### 6. Financial Modeling Prep (Free Tier)
**Cost:** FREE (250 requests/day)
**Rate Limit:** 250/day
**Auth Required:** API key
**Data Quality:** ⭐⭐⭐⭐

**Endpoint:**
```
GET https://financialmodelingprep.com/api/v3/insider-trading?symbol=AAPL&apikey=YOUR_KEY
```

**Response:** JSON with insider trades

**Best For:** Prototyping, limited use

#### 7. Yahoo Finance (Unofficial)
**Cost:** FREE
**Auth Required:** No
**Data Quality:** ⭐⭐⭐

**Limitations:**
- No official API
- May break without notice
- Rate limiting

**Best For:** Testing, learning

### Freemium Sources

#### 1. Quiver Quantitative
**URL:** https://www.quiverquant.com/

**Pricing:**
- Free tier: Limited data
- Premium: $40/month

**Features:**
- Congress trading data
- Insider trading
- Government contracts
- Hedge fund filings

**API:** Available

#### 2. WhaleWisdom
**URL:** https://whalewisdom.com/

**Focus:** 13F filings (institutional holdings)

**Insider Data:** Limited

#### 3. MarketWatch
**URL:** https://www.marketwatch.com/tools/insider-trading

**Features:** Free insider trading search

---

## Code Examples

### Python Examples

#### 1. SEC EDGAR - Fetch Form 4 Filings

```python
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import pandas as pd

class SECInsiderTrading:
    """Fetch SEC Form 4 insider trading data"""

    BASE_URL = "https://www.sec.gov"
    HEADERS = {
        'User-Agent': 'Your Name (your.email@example.com)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_cik_from_ticker(self, ticker):
        """Convert stock ticker to CIK"""
        url = f"{self.BASE_URL}/files/company_tickers.json"
        response = self.session.get(url)
        data = response.json()

        for item in data.values():
            if item['ticker'].upper() == ticker.upper():
                return str(item['cik_str']).zfill(10)
        return None

    def get_company_submissions(self, cik):
        """Get all filings for a company"""
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = self.session.get(url)
        return response.json()

    def get_form4_filings(self, ticker, days_back=30):
        """Get recent Form 4 filings for a ticker"""
        cik = self.get_cik_from_ticker(ticker)
        if not cik:
            raise ValueError(f"Ticker {ticker} not found")

        data = self.get_company_submissions(cik)

        # Filter for Form 4 filings
        filings = data['filings']['recent']
        df = pd.DataFrame({
            'accession_number': filings['accessionNumber'],
            'filing_date': filings['filingDate'],
            'form': filings['form']
        })

        # Filter Form 4
        form4 = df[df['form'] == '4'].copy()
        form4['filing_date'] = pd.to_datetime(form4['filing_date'])

        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days_back)
        form4 = form4[form4['filing_date'] >= cutoff_date]

        return form4

    def download_form4(self, cik, accession_number):
        """Download full Form 4 filing"""
        # Convert accession number to path format
        acc_clean = accession_number.replace('-', '')

        url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{acc_clean}.txt"
        response = self.session.get(url)
        return response.text

# Usage Example
sec = SECInsiderTrading()

# Get Form 4 filings for Apple
ticker = "AAPL"
form4_filings = sec.get_form4_filings(ticker, days_back=30)

print(f"Recent Form 4 filings for {ticker}:")
print(form4_filings)

# Download specific filing
if not form4_filings.empty:
    cik = sec.get_cik_from_ticker(ticker)
    accession = form4_filings.iloc[0]['accession_number']
    filing_text = sec.download_form4(cik, accession)
    print(f"\nFiling text preview:\n{filing_text[:500]}")
```

#### 2. Parse Form 4 XML

```python
import xml.etree.ElementTree as ET

def parse_form4_xml(xml_content):
    """Parse SEC Form 4 XML and extract transactions"""

    # Find XML content in submission (it's within the text file)
    lines = xml_content.split('\n')
    xml_start = None
    xml_end = None

    for i, line in enumerate(lines):
        if '<XML>' in line:
            xml_start = i
        elif '</XML>' in line:
            xml_end = i
            break

    if xml_start is None or xml_end is None:
        return []

    xml_text = '\n'.join(lines[xml_start+1:xml_end])

    # Parse XML
    root = ET.fromstring(xml_text)

    # Define namespace
    ns = {'ns': 'http://www.sec.gov/edgar/document/thirteenf/informationtable'}

    transactions = []

    # Extract non-derivative transactions (common stock)
    for non_deriv in root.findall('.//nonDerivativeTransaction'):
        transaction = {
            'security': root.find('.//issuingOwner').find('issuingOwnerName').text if root.find('.//issuingOwner') else 'N/A',
            'transaction_date': non_deriv.find('.//transactionDate').find('date').text if non_deriv.find('.//transactionDate') is not None else 'N/A',
            'transaction_code': non_deriv.find('.//transactionCoding').find('transactionCode').text if non_deriv.find('.//transactionCoding') is not None else 'N/A',
            'shares': float(non_deriv.find('.//transactionAmounts').find('transactionShares').find('value').text) if non_deriv.find('.//transactionAmounts') is not None else 0,
            'price_per_share': float(non_deriv.find('.//transactionAmounts').find('transactionPricePerShare').find('value').text) if non_deriv.find('.//transactionAmounts') is not None else 0,
            'total_value': 0
        }

        transaction['total_value'] = transaction['shares'] * transaction['price_per_share']
        transactions.append(transaction)

    return pd.DataFrame(transactions)

# Usage
# df_transactions = parse_form4_xml(filing_text)
# print(df_transactions)
```

#### 3. Insider Trading Signal Detector

```python
import pandas as pd
from datetime import datetime, timedelta

class InsiderSignalDetector:
    """Detect bullish/bearish insider trading signals"""

    def __init__(self):
        self.signals = []

    def analyze_transaction(self, transaction):
        """
        Analyze a single transaction for signals

        Returns: 'BULLISH', 'BEARISH', or 'NEUTRAL'
        """
        score = 0

        # Transaction type scoring
        if transaction['transaction_code'] == 'P':  # Purchase
            score += 2
        elif transaction['transaction_code'] == 'S':  # Sale
            score -= 1
        elif transaction['transaction_code'] == 'A':  # Award
            score += 1  # Neutral to slightly bullish

        # Size scoring (relative to typical ranges)
        value = transaction.get('total_value', 0)
        if value > 1000000:  # >$1M
            score += 2
        elif value > 100000:  # >$100k
            score += 1

        # Ownership percentage change
        ownership_change = transaction.get('ownership_percentage_change', 0)
        if ownership_change > 0.05:  # >5% increase
            score += 2
        elif ownership_change > 0.01:  # >1% increase
            score += 1
        elif ownership_change < -0.01:  # Decrease
            score -= 1

        # Position scoring
        position = transaction.get('position', '').lower()
        if 'ceo' in position or 'cfo' in position:
            score += 2  # More weight on executives
        elif 'director' in position:
            score += 1

        # Determine signal
        if score >= 4:
            return 'STRONG_BUY'
        elif score >= 2:
            return 'BUY'
        elif score >= 0:
            return 'NEUTRAL'
        elif score >= -2:
            return 'SELL'
        else:
            return 'STRONG_SELL'

    def generate_signals(self, transactions_df):
        """Generate signals from multiple transactions"""
        signals = []

        for _, transaction in transactions_df.iterrows():
            signal = self.analyze_transaction(transaction.to_dict())
            signals.append({
                'date': transaction.get('transaction_date'),
                'insider': transaction.get('insider_name', 'N/A'),
                'position': transaction.get('position', 'N/A'),
                'ticker': transaction.get('ticker', 'N/A'),
                'transaction_type': transaction.get('transaction_code'),
                'shares': transaction.get('shares', 0),
                'value': transaction.get('total_value', 0),
                'signal': signal,
                'timestamp': datetime.now()
            })

        return pd.DataFrame(signals)

# Usage
detector = InsiderSignalDetector()

# Example transaction
example_transaction = {
    'transaction_code': 'P',  # Purchase
    'total_value': 500000,  # $500k
    'ownership_percentage_change': 0.08,  # 8% increase
    'position': 'CEO',
    'transaction_date': '2026-02-06',
    'insider_name': 'John Doe',
    'ticker': 'AAPL'
}

signal = detector.analyze_transaction(example_transaction)
print(f"Signal: {signal}")
```

#### 4. Batch Processing - Multiple Tickers

```python
import time
import pandas as pd
from typing import List

def batch_fetch_insider_trading(tickers: List[str], days_back: int = 30):
    """
    Fetch insider trading data for multiple tickers

    Args:
        tickers: List of stock tickers
        days_back: Number of days to look back

    Returns:
        DataFrame with all insider trades
    """
    sec = SECInsiderTrading()
    all_transactions = []

    for ticker in tickers:
        try:
            print(f"Fetching {ticker}...")

            # Get filings
            filings = sec.get_form4_filings(ticker, days_back=days_back)

            if filings.empty:
                print(f"  No Form 4 filings found for {ticker}")
                continue

            # Get CIK
            cik = sec.get_cik_from_ticker(ticker)

            # Download and parse each filing
            for _, filing in filings.iterrows():
                try:
                    filing_text = sec.download_form4(cik, filing['accession_number'])
                    # Parse and extract transactions
                    # transactions = parse_form4_xml(filing_text)
                    # Add ticker info
                    # transactions['ticker'] = ticker
                    # all_transactions.append(transactions)

                    time.sleep(0.1)  # Be nice to SEC servers

                except Exception as e:
                    print(f"  Error parsing filing: {e}")

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue

        time.sleep(1)  # Rate limiting between tickers

    # Combine all transactions
    if all_transactions:
        return pd.concat(all_transactions, ignore_index=True)
    else:
        return pd.DataFrame()

# Usage
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
insider_data = batch_fetch_insider_trading(tickers, days_back=30)
print(insider_data.head())
```

### JavaScript/Node.js Examples

#### 5. SEC EDGAR API - Node.js

```javascript
const axios = require('axios');

class SECInsiderTrading {
    constructor() {
        this.baseUrl = 'https://www.sec.gov';
        this.headers = {
            'User-Agent': 'Your Name (your.email@example.com)',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json'
        };
    }

    async getCIKFromTicker(ticker) {
        const url = `${this.baseUrl}/files/company_tickers.json`;
        const response = await axios.get(url, { headers: this.headers });

        for (const [key, value] of Object.entries(response.data)) {
            if (value.ticker.toUpperCase() === ticker.toUpperCase()) {
                return value.cik_str.toString().padStart(10, '0');
            }
        }
        return null;
    }

    async getCompanySubmissions(cik) {
        const url = `https://data.sec.gov/submissions/CIK${cik}.json`;
        const response = await axios.get(url, { headers: this.headers });
        return response.data;
    }

    async getForm4Filings(ticker, daysBack = 30) {
        const cik = await this.getCIKFromTicker(ticker);
        if (!cik) {
            throw new Error(`Ticker ${ticker} not found`);
        }

        const data = await this.getCompanySubmissions(cik);
        const filings = data.filings.recent;

        // Create array of objects
        const form4Filings = [];
        for (let i = 0; i < filings.form.length; i++) {
            if (filings.form[i] === '4') {
                form4Filings.push({
                    accessionNumber: filings.accessionNumber[i],
                    filingDate: filings.filingDate[i],
                    form: filings.form[i]
                });
            }
        }

        // Filter by date
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - daysBack);

        return form4Filings.filter(f => new Date(f.filingDate) >= cutoffDate);
    }

    async downloadForm4(cik, accessionNumber) {
        const accClean = accessionNumber.replace(/-/g, '');
        const url = `${this.baseUrl}/Archives/edgar/data/${cik}/${accClean}.txt`;
        const response = await axios.get(url, { headers: this.headers });
        return response.data;
    }
}

// Usage
(async () => {
    const sec = new SECInsiderTrading();

    try {
        const filings = await sec.getForm4Filings('AAPL', 30);
        console.log('Recent Form 4 filings for AAPL:', filings);

        if (filings.length > 0) {
            const cik = await sec.getCIKFromTicker('AAPL');
            const filingText = await sec.downloadForm4(cik, filings[0].accessionNumber);
            console.log('\nFiling text preview:', filingText.substring(0, 500));
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
```

#### 6. Web Scraping - OpenInsider (with proper attribution)

```javascript
const axios = require('axios');
const cheerio = require('cheerio');
const { Parser } = require('json2csv');

async function scrapeOpenInsider(ticker) {
    const url = `https://www.openinsider.com/screener?s=${ticker}`;

    const headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; InsiderBot/1.0)',
        'Referer': 'https://www.openinsider.com/'
    };

    try {
        const response = await axios.get(url, { headers });
        const $ = cheerio.load(response.data);

        const insiderData = [];

        // Parse table rows (actual selectors may vary)
        $('table.insider-table tbody tr').each((i, element) => {
            const $row = $(element);

            insiderData.push({
                filingDate: $row.find('td:nth-child(1)').text().trim(),
                tradeDate: $row.find('td:nth-child(2)').text().trim(),
                ticker: $row.find('td:nth-child(3)').text().trim(),
                insiderName: $row.find('td:nth-child(4)').text().trim(),
                position: $row.find('td:nth-child(5)').text().trim(),
                transactionType: $row.find('td:nth-child(6)').text().trim(),
                shares: parseInt($row.find('td:nth-child(7)').text().replace(/,/g, '')),
                price: parseFloat($row.find('td:nth-child(8)').text().replace(/[$,]/g, '')),
                totalValue: parseFloat($row.find('td:nth-child(9)').text().replace(/[$,]/g, '')),
                ownershipPercent: parseFloat($row.find('td:nth-child(10)').text().replace(/%/g, ''))
            });
        });

        return insiderData;

    } catch (error) {
        console.error('Scraping error:', error.message);
        return [];
    }
}

// Usage
(async () => {
    const data = await scrapeOpenInsider('AAPL');
    console.log(`Found ${data.length} insider trades for AAPL`);
    console.log(data[0]);
})();
```

### API Integration Examples

#### 7. Telegram Alerts for Insider Trading

```python
import requests
from datetime import datetime

class InsiderTradingAlerts:
    """Send insider trading signals to Telegram"""

    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, message):
        """Send message to Telegram"""
        url = f"{self.api_url}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        response = requests.post(url, json=data)
        return response.json()

    def format_insider_alert(self, transaction, signal):
        """Format insider trading alert for Telegram"""

        emoji = {
            'STRONG_BUY': '🚀🚀🚀',
            'BUY': '🚀',
            'NEUTRAL': '➡️',
            'SELL': '⚠️',
            'STRONG_SELL': '🔴🔴🔴'
        }

        message = f"""
<b>🔔 Insider Trading Alert</b>

{emoji.get(signal, '📊')} <b>Signal:</b> {signal}

<b>📈 Ticker:</b> {transaction.get('ticker')}
<b>👤 Insider:</b> {transaction.get('insider_name')}
<b>💼 Position:</b> {transaction.get('position')}

<b>📊 Transaction:</b>
• Type: {transaction.get('transaction_code')}
• Shares: {transaction.get('shares'):,.0f}
• Value: ${transaction.get('value', 0):,.2f}
• Date: {transaction.get('transaction_date')}

<i>Data Source: SEC EDGAR</i>
<i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        return message

    def send_insider_alert(self, transaction, signal):
        """Send formatted insider trading alert"""
        message = self.format_insider_alert(transaction, signal)
        return self.send_message(message)

# Usage
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

alerts = InsiderTradingAlerts(BOT_TOKEN, CHAT_ID)

# Example alert
transaction = {
    'ticker': 'AAPL',
    'insider_name': 'Tim Cook',
    'position': 'CEO',
    'transaction_code': 'P',
    'shares': 10000,
    'value': 1500000,
    'transaction_date': '2026-02-06'
}

alerts.send_insider_alert(transaction, 'STRONG_BUY')
```

#### 8. Store in Database (PostgreSQL)

```python
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class InsiderTradingDB:
    """Store and query insider trading data in PostgreSQL"""

    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def create_tables(self):
        """Create database tables"""

        # Companies table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                cik VARCHAR(10) PRIMARY KEY,
                ticker VARCHAR(10) UNIQUE NOT NULL,
                company_name VARCHAR(255),
                exchange VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Insiders table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS insiders (
                id SERIAL PRIMARY KEY,
                cik VARCHAR(10),
                insider_name VARCHAR(255) NOT NULL,
                position VARCHAR(100),
                FOREIGN KEY (cik) REFERENCES companies(cik)
            );
        """)

        # Transactions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS insider_transactions (
                id SERIAL PRIMARY KEY,
                cik VARCHAR(10),
                accession_number VARCHAR(50),
                transaction_date DATE,
                filing_date DATE,
                transaction_code VARCHAR(1),
                shares NUMERIC(20, 2),
                price_per_share NUMERIC(10, 4),
                total_value NUMERIC(20, 2),
                ownership_before NUMERIC(10, 4),
                ownership_after NUMERIC(10, 4),
                signal VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cik) REFERENCES companies(cik)
            );
        """)

        # Create indexes
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ticker ON companies(ticker);
            CREATE INDEX IF NOT EXISTS idx_transaction_date ON insider_transactions(transaction_date);
            CREATE INDEX IF NOT EXISTS idx_filing_date ON insider_transactions(filing_date);
            CREATE INDEX IF NOT EXISTS idx_signal ON insider_transactions(signal);
        """)

        self.conn.commit()

    def insert_transaction(self, transaction_data):
        """Insert a transaction record"""
        self.cursor.execute("""
            INSERT INTO insider_transactions
            (cik, accession_number, transaction_date, filing_date,
             transaction_code, shares, price_per_share, total_value, signal)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (accession_number) DO NOTHING
        """, (
            transaction_data['cik'],
            transaction_data['accession_number'],
            transaction_data['transaction_date'],
            transaction_data['filing_date'],
            transaction_data['transaction_code'],
            transaction_data['shares'],
            transaction_data['price_per_share'],
            transaction_data['total_value'],
            transaction_data.get('signal')
        ))
        self.conn.commit()

    def get_recent_signals(self, ticker, days_back=7, min_signal='BUY'):
        """Get recent bullish signals for a ticker"""
        self.cursor.execute("""
            SELECT it.*, c.ticker, c.company_name
            FROM insider_transactions it
            JOIN companies c ON it.cik = c.cik
            WHERE c.ticker = %s
            AND it.transaction_date >= CURRENT_DATE - INTERVAL '%s days'
            AND it.signal >= %s
            ORDER BY it.transaction_date DESC
        """, (ticker, days_back, min_signal))

        return self.cursor.fetchall()

    def get_top_insider_buys(self, limit=10):
        """Get top insider buys by value"""
        self.cursor.execute("""
            SELECT it.*, c.ticker, c.company_name
            FROM insider_transactions it
            JOIN companies c ON it.cik = c.cik
            WHERE it.transaction_code = 'P'
            AND it.transaction_date >= CURRENT_DATE - INTERVAL '7 days'
            ORDER BY it.total_value DESC
            LIMIT %s
        """, (limit,))

        return self.cursor.fetchall()

    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()

# Usage
db = InsiderTradingDB('insider_trading', 'postgres', 'password')
db.create_tables()

# Insert a transaction
db.insert_transaction({
    'cik': '0000320193',
    'accession_number': '0000320193-26-000001',
    'transaction_date': '2026-02-06',
    'filing_date': '2026-02-07',
    'transaction_code': 'P',
    'shares': 10000,
    'price_per_share': 150.25,
    'total_value': 1502500.00,
    'signal': 'STRONG_BUY'
})

# Query recent signals
signals = db.get_recent_signals('AAPL', days_back=7)
for signal in signals:
    print(f"{signal['ticker']}: {signal['signal']} - ${signal['total_value']:,.2f}")

db.close()
```

---

## Rate Limits & Best Practices

### SEC EDGAR Rate Limits

**Official Limits:**
- **10 requests per second** per IP address
- **No authentication required** but User-Agent mandatory
- **Request bursts** may trigger temporary blocks

**Best Practices:**

1. **Always include User-Agent header**
   ```python
   headers = {
       'User-Agent': 'Your Name (your.email@example.com)',
       'Accept-Encoding': 'gzip, deflate'
   }
   ```

2. **Implement rate limiting**
   ```python
   import time

   def rate_limit_request(url, delay=0.2):  # 5 requests per second
       time.sleep(delay)
       return requests.get(url, headers=headers)
   ```

3. **Use caching**
   ```python
   import functools
   from datetime import datetime, timedelta

   @functools.lru_cache(maxsize=1000)
   def cached_get_cik(ticker, date):
       # Fetch CIK (cached per day)
       pass
   ```

4. **Batch requests efficiently**
   ```python
   def batch_with_delay(items, batch_size=10, delay=2):
       results = []
       for i in range(0, len(items), batch_size):
           batch = items[i:i+batch_size]
           for item in batch:
               results.append(fetch_data(item))
               time.sleep(0.2)  # 5 per second
           time.sleep(delay)  # Pause between batches
       return results
   ```

5. **Handle errors gracefully**
   ```python
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry

   session = requests.Session()
   retry = Retry(total=3, backoff_factor=1)
   adapter = HTTPAdapter(max_retries=retry)
   session.mount('https://', adapter)
   ```

### Commercial API Alternatives

If you need higher rate limits or better reliability:

#### 1. Financial Modeling Prep
**URL:** https://financialmodelingprep.com/

**Pricing:**
- Free: 250 requests/day
- Starter: $24/month (10,000 requests/month)
- Professional: $79/month (100,000 requests/month)

**Insider Trading Endpoint:**
```
GET https://financialmodelingprep.com/api/v3/insider-trading?symbol=AAPL&apikey=YOUR_KEY
```

#### 2. IEX Cloud
**URL:** https://iexcloud.io/

**Pricing:**
- Free: 100,000 calls/month
- Grow: $9/month (500,000 calls/month)
**Note:** Insider data not available on free tier

#### 3. Quiver Quantitative
**URL:** https://www.quiverquant.com/

**Features:**
- Congress trading
- Insider trading
- Government contracts

**Pricing:** $40/month

#### 4. Polygon.io
**URL:** https://polygon.io/

**Pricing:**
- Free: Limited
- Starter: $49/month

**Note:** Check current insider data availability

### Data Refresh Schedule

**Real-time Updates:**
- SEC filings: As filed (delays 1-2 minutes)
- Aggregators: 5-15 minute delays

**Daily Updates:**
- SEC daily index: Updated at 5 AM ET
- Most free APIs: Daily refresh

**Weekly Updates:**
- Some free sources: Weekly bulk downloads

### Data Storage Strategy

```python
# Database schema recommendation
CREATE TABLE insider_transactions (
    id SERIAL PRIMARY KEY,
    cik VARCHAR(10),
    ticker VARCHAR(10),
    insider_name VARCHAR(255),
    position VARCHAR(100),
    transaction_date DATE,
    filing_date DATE,
    transaction_code VARCHAR(1),
    shares NUMERIC(20, 2),
    price_per_share NUMERIC(10, 4),
    total_value NUMERIC(20, 2),
    ownership_before NUMERIC(10, 4),
    ownership_after NUMERIC(10, 4),
    signal VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_ticker ON insider_transactions(ticker);
CREATE INDEX idx_transaction_date ON insider_transactions(transaction_date);
CREATE INDEX idx_filing_date ON insider_transactions(filing_date);
CREATE INDEX idx_signal ON insider_transactions(signal);
CREATE INDEX idx_insider_name ON insider_transactions(insider_name);
```

### Monitoring & Maintenance

**Daily Tasks:**
- Fetch new Form 4 filings
- Update company/ticker mappings
- Calculate signals
- Send alerts

**Weekly Tasks:**
- Clean up old data
- Archive historical data
- Review rate limit usage
- Check for broken URLs

**Monthly Tasks:**
- Update CIK mappings
- Review and optimize queries
- Check data quality
- Update documentation

---

## Summary & Recommendations

### Best Free Options

1. **SEC EDGAR API** (Best overall)
   - Official, accurate, comprehensive
   - Requires parsing
   - 10 requests/second limit

2. **OpenInsider** (Easiest to use)
   - Clean interface
   - Good for manual checks
   - No official API

3. **Finviz** (Quick overview)
   - Free with registration
   - Limited historical data

### For Production Use

**Recommended Stack:**
- **Data Source:** SEC EDGAR API (primary) + OpenInsider (backup)
- **Storage:** PostgreSQL or MongoDB
- **Processing:** Python (pandas, requests)
- **Alerts:** Telegram, Slack, or Email
- **Visualization:** Grafana or custom dashboard

### Integration with Trading Systems

**How to integrate insider trading data into your Oneshot FTMO system:**

1. **As an additional filter** - Only trade when insiders are buying
2. **For sentiment analysis** - Combine with ATF signals
3. **For stock selection** - Focus on stocks with strong insider buying
4. **For position sizing** - Increase size when multiple insiders buy

**Example integration points:**
```python
# In your Oneshot_FTMO.mq5 or Oneshot_AutoTrader.cs
bool CheckInsiderSentiment(string ticker) {
    // Call your insider trading API
    // Return true if recent insider buying detected
    return GetRecentInsiderBuys(ticker, days_back=30) > 2;
}
```

### Legal & Compliance Notes

- **Insider trading data is public information** - Using it is legal
- **Don't confuse with insider trading** - Using public disclosures is not insider trading
- **Always verify data** - Errors can occur in filings
- **Respect rate limits** - Essential for continued access
- **Cite sources** - When distributing data

---

## Additional Resources

### Documentation
- [SEC EDGAR API Documentation](https://www.sec.gov/edgar/sec-api-documentation)
- [Form 4 Filing Instructions](https://www.sec.gov/files/form4-instructions.pdf)
- [MAR Implementation Guidelines](https://www.esma.europa.eu/market-abuse-regulation-mar)

### Tools & Libraries
- **Python:** requests, pandas, sqlalchemy
- **Node.js:** axios, cheerio
- **Database:** PostgreSQL, MongoDB

### Communities
- Reddit: r/algotrading, r/stocks
- Discord: Trading servers
- GitHub: Open source trading bots

---

**Last Updated:** February 6, 2026
**Version:** 1.0

For questions or updates, please refer to official SEC documentation and API references.
