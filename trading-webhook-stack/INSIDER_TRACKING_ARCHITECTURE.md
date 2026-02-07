# 🎯 Insider Trading Tracking Application - Complete Architecture Guide

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Data Pipeline](#data-pipeline)
4. [Database Design](#database-design)
5. [Backend Implementation](#backend-implementation)
6. [n8n Workflow Integration](#n8n-workflow-integration)
7. [Frontend Dashboard](#frontend-dashboard)
8. [Deployment Options](#deployment-options)
9. [Code Examples](#code-examples)
10. [Best Practices](#best-practices)

---

## Overview

This guide provides a **production-ready architecture** for tracking insider trading activities, SEC filings, and corporate insider transactions. The system monitors multiple data sources, processes filings in real-time, filters based on user criteria, and sends notifications via Telegram.

### Key Features

- **Real-time SEC filing monitoring** (Form 4, Form 3, Form 5)
- **Corporate insider tracking** (CEO, CFO, CTO, directors)
- **Transaction filtering** (buys only, sells only, minimum amounts)
- **Smart notification system** (Telegram alerts)
- **Historical data analysis** (trends, patterns)
- **Dashboard UI** (visualize insider activity)
- **API access** (integrations with trading systems)
- **Multi-source data aggregation** (SEC, FINRA, company filings)

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ SEC EDGAR    │  │ FINRA       │  │ Company      │                 │
│  │ API          │  │ Disclosures │  │ Filings      │                 │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│         │                 │                 │                          │
└─────────┼─────────────────┼─────────────────┼──────────────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SEC Scraper Service                                             │   │
│  │  - Python scraper for SEC EDGAR                                  │   │
│  │  - Rate limiting (10 requests/second per SEC rules)             │   │
│  │  - Incremental updates (only new filings)                       │   │
│  │  - Error handling & retry logic                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  n8n Workflow Automation                                         │   │
│  │  - Webhook receivers for external sources                        │   │
│  │  - Data transformation & normalization                          │   │
│  │  - Integration hub for multiple sources                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Message Queue (Redis/Bull)                                      │   │
│  │  - Async processing                                              │   │
│  │  - Job scheduling                                               │   │
│  │  - Retry mechanism                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Data Processor Service                                          │   │
│  │  - Parse SEC filings (XML/JSON)                                  │   │
│  │  - Extract insider transactions                                   │   │
│  │  - Normalize data format                                          │   │
│  │  - Apply user filters                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  PostgreSQL Database                                             │   │
│  │  - Companies table                                               │   │
│  │  - Insiders table                                                │   │
│  │  - Transactions table                                            │   │
│  │  - Filings table                                                 │   │
│  │  - User filters table                                            │   │
│  │  - Alerts history table                                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Redis Cache                                                      │   │
│  │  - Recent filings cache                                          │   │
│  │  - Rate limiting counters                                        │   │
│  │  - Session data                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    API & NOTIFICATION LAYER                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  REST API (Express.js)                                           │   │
│  │  - GET /api/insiders - List insiders                             │   │
│  │  - GET /api/transactions - Get transactions                      │   │
│  │  - GET /api/filings - Get filings                                │   │
│  │  - POST /api/filters - Create filter                             │   │
│  │  - GET /api/alerts - Get alert history                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Notification Service                                             │   │
│  │  - Telegram bot integration                                       │   │
│  │  - Email notifications (optional)                                 │   │
│  │  - Webhook callbacks                                              │   │
│  │  - Alert throttling & deduplication                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Web Dashboard (React/Next.js)                                    │   │
│  │  - Insider activity feed                                          │   │
│  │  - Transaction search & filters                                   │   │
│  │  - Company profiles                                               │   │
│  │  - Insider ranking                                                │   │
│  │  - Historical charts                                              │   │
│  │  - User filter management                                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Pipeline

### Complete Data Flow

```
1. DATA ACQUISITION
   │
   ├──> SEC EDGAR API (Polling every 5 minutes)
   │    ├──> Form 4 (Statement of changes in ownership)
   │    ├──> Form 3 (Initial statement of ownership)
   │    └──> Form 5 (Annual statement of ownership)
   │
   ├──> FINRA Disclosures (Webhook/API)
   │    └──> Insider trading reports
   │
   └──> Company Press Releases (RSS/Web scraping)
        └──> Insider transaction announcements

2. DATA COLLECTION
   │
   ├──> Python SEC Scraper
   │    ├──> Fetch new filings (incremental)
   │    ├──> Parse XML/JSON data
   │    ├──> Extract relevant fields
   │    └──> Send to message queue
   │
   └──> n8n Webhook Receiver
        ├──> Receive external data
        ├──> Transform/normalize
        └──> Send to message queue

3. DATA PROCESSING
   │
   ├──> Message Queue (Redis/Bull)
   │    ├──> Queue jobs for processing
   │    ├──> Retry failed jobs
   │    └── Worker pool management
   │
   └──> Data Processor Service
        ├──> Parse insider transactions
        ├──> Identify key insiders (CEO, CFO, etc.)
        ├──> Calculate transaction values
        ├──> Apply user filters
        └──> Score transactions (importance)

4. DATA STORAGE
   │
   ├──> PostgreSQL Database
   │    ├──> Store raw filings
   │    ├──> Store processed transactions
   │    ├──> Update insider profiles
   │    └── Maintain historical data
   │
   └──> Redis Cache
        ├──> Cache recent filings (24h)
        ├──> Rate limiting
        └── Session data

5. FILTERING & ALERTING
   │
   ├──> Filter Engine
   │    ├──> Check user-defined filters
   │    ├──> Match conditions:
   │    │   ├──> Insider role (CEO, CFO, etc.)
   │    │   ├──> Transaction type (buy/sell)
   │    │   ├──> Minimum amount ($50k, $100k, etc.)
   │    │   ├──> Company ticker/sector
   │    │   └── Time-based filters
   │    └──> Score relevance
   │
   └──> Alert Service
         ├──> Check if filter matches
         ├──> Deduplicate alerts
         ├──> Throttle notifications
         └──> Send to Telegram/Email/Webhook

6. NOTIFICATION DELIVERY
   │
   ├──> Telegram Bot
   │    ├──> Format message with emoji
   │    ├──> Include transaction details
   │    ├──> Add relevant links
   │    └──> Send to user chat
   │
   ├──> Email Service (optional)
   │    ├──> HTML email template
   │    ├──> Attach relevant documents
   │    └──> Send to subscriber list
   │
   └──> Webhook Callbacks
         └──> POST to registered endpoints

7. DASHBOARD UPDATE
   │
   └──> WebSocket/Server-Sent Events
        ├──> Push real-time updates
        ├──> Update activity feed
        └──> Refresh statistics
```

---

## Database Design

### PostgreSQL Schema

```sql
-- Companies table
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    cik VARCHAR(10) UNIQUE NOT NULL,  -- SEC Central Index Key
    company_name VARCHAR(255) NOT NULL,
    exchange VARCHAR(50),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insiders table
CREATE TABLE insiders (
    id SERIAL PRIMARY KEY,
    cik VARCHAR(10) UNIQUE NOT NULL,
    company_id INTEGER REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    title VARCHAR(100),  -- CEO, CFO, CTO, Director, etc.
    is_officer BOOLEAN DEFAULT FALSE,
    is_director BOOLEAN DEFAULT FALSE,
    is_10_percent_owner BOOLEAN DEFAULT FALSE,
    transactions_count INTEGER DEFAULT 0,
    last_transaction_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    insider_id INTEGER REFERENCES insiders(id),
    company_id INTEGER REFERENCES companies(id),
    filing_type VARCHAR(10) NOT NULL,  -- Form 3, 4, 5
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,  -- Buy, Sell, Option Exercise, etc.
    shares_traded DECIMAL(15, 2) NOT NULL,
    price_per_share DECIMAL(10, 4),
    total_value DECIMAL(15, 2),
    shares_owned_after_transaction DECIMAL(15, 2),
    ownership_type VARCHAR(50),  -- Direct, Indirect
    sec_file_url TEXT,
    filing_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indexes for performance
    CONSTRAINT chk_transaction_type CHECK (transaction_type IN ('P', 'S', 'M', 'A', 'D', 'G', 'F')),
    CONSTRAINT chk_filing_type CHECK (filing_type IN ('3', '4', '5'))
);

-- Filings table (raw SEC filing data)
CREATE TABLE filings (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    insider_id INTEGER REFERENCES insiders(id),
    filing_type VARCHAR(10) NOT NULL,
    filing_date DATE NOT NULL,
    sec_accession_number VARCHAR(50) UNIQUE NOT NULL,
    sec_file_url TEXT NOT NULL,
    raw_data JSONB,  -- Store complete filing data
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User filters table
CREATE TABLE user_filters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,  -- Telegram chat ID or user ID
    filter_name VARCHAR(100),
    insider_titles VARCHAR(255)[],  -- ['CEO', 'CFO', 'CTO']
    transaction_types VARCHAR(50)[],  -- ['buy', 'sell']
    min_transaction_value DECIMAL(15, 2),
    companies VARCHAR(10)[],  -- ['AAPL', 'TSLA', 'MSFT']
    sectors VARCHAR(100)[],
    is_active BOOLEAN DEFAULT TRUE,
    notification_method VARCHAR(50) DEFAULT 'telegram',  -- telegram, email, webhook
    webhook_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alert history table
CREATE TABLE alert_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    filter_id INTEGER REFERENCES user_filters(id),
    transaction_id INTEGER REFERENCES transactions(id),
    alert_type VARCHAR(50),  -- telegram, email, webhook
    status VARCHAR(50),  -- sent, failed, pending
    error_message TEXT,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Statistics table (cached for performance)
CREATE TABLE statistics (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    total_filings INTEGER DEFAULT 0,
    total_transactions INTEGER DEFAULT 0,
    unique_insiders INTEGER DEFAULT 0,
    unique_companies INTEGER DEFAULT 0,
    total_buy_value DECIMAL(15, 2),
    total_sell_value DECIMAL(15, 2),
    top_insider_id INTEGER,
    top_company_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_insider ON transactions(insider_id);
CREATE INDEX idx_transactions_company ON transactions(company_id);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_filings_date ON filings(filing_date);
CREATE INDEX idx_filings_company ON filings(company_id);
CREATE INDEX idx_insiders_company ON insiders(company_id);
CREATE INDEX idx_insiders_title ON insiders(title);
CREATE INDEX idx_alerts_user ON alert_history(user_id);
CREATE INDEX idx_alerts_date ON alert_history(created_at);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_insiders_updated_at BEFORE UPDATE ON insiders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_filters_updated_at BEFORE UPDATE ON user_filters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## Backend Implementation

### Project Structure

```
insider-tracking/
├── backend/
│   ├── server.js                 # Express server
│   ├── config/
│   │   ├── database.js           # PostgreSQL config
│   │   ├── redis.js              # Redis config
│   │   └── sec.js                # SEC API config
│   ├── routes/
│   │   ├── api.js                # API routes
│   │   ├── filings.js            # SEC filing routes
│   │   └── filters.js            # User filter routes
│   ├── services/
│   │   ├── secScraper.js         # SEC scraping service
│   │   ├── dataProcessor.js      # Data processing service
│   │   ├── filterEngine.js       # Filter matching engine
│   │   ├── alertService.js       # Alert/notification service
│   │   └── telegram.js           # Telegram bot (reuse existing)
│   ├── workers/
│   │   ├── queue.js              # Bull queue setup
│   │   ├── secWorker.js          # SEC filing processor
│   │   └── notificationWorker.js # Alert sender
│   ├── models/
│   │   ├── Company.js
│   │   ├── Insider.js
│   │   ├── Transaction.js
│   │   ├── Filing.js
│   │   └── UserFilter.js
│   ├── utils/
│   │   ├── logger.js             # Reuse existing
│   │   ├── dateHelper.js         # Date utilities
│   │   └── secParser.js          # SEC XML parser
│   └── middleware/
│       ├── auth.js               # Authentication
│       └── rateLimiter.js        # Rate limiting
├── scrapers/
│   ├── secScraper.py             # Python SEC scraper
│   ├── requirements.txt
│   └── config.py
├── n8n-workflows/
│   ├── sec-webhook.json          # n8n workflow for SEC data
│   ├── filter-workflow.json      # n8n workflow for filtering
│   └── notification-workflow.json
├── frontend/
│   └── (dashboard code)
└── docker-compose.yml
```

### Key Backend Components

#### 1. SEC Scraper Service (Python)

`scrapers/secScraper.py`:

```python
#!/usr/bin/env python3
"""
SEC EDGAR Filings Scraper
Monitors SEC filings for insider trading activity
"""

import requests
import xml.etree.ElementTree as ET
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import redis
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SECScraper:
    """
    SEC EDGAR API Scraper
    Follows SEC rate limiting rules (10 requests/second)
    """

    def __init__(self, redis_host='localhost', redis_port=6379):
        self.base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        self.submissions_url = "https://data.sec.gov/submissions"
        self.headers = {
            'User-Agent': 'InsiderTracker/1.0 (your-email@example.com)',  # SEC requires User-Agent
            'Accept': 'application/json'
        }
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.rate_limit_delay = 0.1  # 10 requests per second = 0.1s delay
        self.last_request_time = 0

    def _rate_limit(self):
        """Implement SEC rate limiting (10 requests/second)"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)

        self.last_request_time = time.time()

    def get_recent_filings(
        self,
        filing_type: str = '4',
        days_back: int = 1,
        count: int = 100
    ) -> List[Dict]:
        """
        Get recent SEC filings

        Args:
            filing_type: Form type (3, 4, or 5)
            days_back: Number of days to look back
            count: Maximum number of filings to return

        Returns:
            List of filing dictionaries
        """
        self._rate_limit()

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # Build query parameters
        params = {
            'action': 'getcompany',
            'type': filing_type,
            'dateb': end_date.strftime('%Y%m%d'),
            'datea': start_date.strftime('%Y%m%d'),
            'owner': 'only',  # Only ownership reports
            'count': count
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers
            )
            response.raise_for_status()

            # Parse HTML response
            soup = BeautifulSoup(response.content, 'html.parser')
            filings = self._parse_filing_table(soup)

            logger.info(f"Retrieved {len(filings)} {filing_type} filings")
            return filings

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching filings: {e}")
            return []

    def get_company_insiders(self, ticker: str) -> List[Dict]:
        """Get all insiders for a specific company"""
        self._rate_limit()

        # Get company CIK (Central Index Key)
        cik = self._get_company_cik(ticker)
        if not cik:
            logger.error(f"Could not find CIK for ticker {ticker}")
            return []

        # Get company submissions
        url = f"{self.submissions_url}/CIK{cik.zfill(10)}.json"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Extract insider information
            insiders = self._parse_insiders(data)
            return insiders

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching insiders for {ticker}: {e}")
            return []

    def parse_filing_xml(self, accession_number: str) -> Optional[Dict]:
        """
        Parse SEC filing XML to extract transaction details

        Args:
            accession_number: SEC accession number

        Returns:
            Dictionary with transaction details
        """
        self._rate_limit()

        # Build XML URL
        # Example: https://www.sec.gov/Archives/edgar/data/320193/000032019323000007/0000320193-23-000007.txt
        parts = accession_number.split('-')
        cik = parts[0].lstrip('0')

        url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-', '')}/{accession_number}.txt"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            # Parse XML content
            root = ET.fromstring(response.content)

            # Extract transaction data
            transactions = self._extract_transactions(root)

            return {
                'accession_number': accession_number,
                'transactions': transactions
            }

        except Exception as e:
            logger.error(f"Error parsing filing {accession_number}: {e}")
            return None

    def _parse_filing_table(self, soup) -> List[Dict]:
        """Parse SEC EDGAR HTML table to extract filing information"""
        filings = []

        table = soup.find('table', class_='tableFile2')
        if not table:
            return filings

        rows = table.find_all('tr')[1:]  # Skip header row

        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 4:
                continue

            filing = {
                'filing_type': cells[0].text.strip(),
                'filing_date': cells[3].text.strip(),
                'filed_by': cells[1].text.strip(),
                'link': 'https://www.sec.gov' + cells[1].find('a')['href']
            }
            filings.append(filing)

        return filings

    def _get_company_cik(self, ticker: str) -> Optional[str]:
        """Get company CIK from ticker symbol"""
        self._rate_limit()

        params = {
            'action': 'getcompany',
            'CIK': ticker
        }

        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()

            # Extract CIK from response
            soup = BeautifulSoup(response.content, 'html.parser')
            cik_span = soup.find('span', {'class': 'companyInfo'})
            if cik_span:
                cik = cik_span.text.split('CIK:')[1].strip()
                return cik

        except Exception as e:
            logger.error(f"Error getting CIK for {ticker}: {e}")

        return None

    def _parse_insiders(self, data: Dict) -> List[Dict]:
        """Parse insider information from company submission data"""
        insiders = []

        # This is a simplified example
        # Real implementation would parse the actual SEC JSON structure
        try:
            for holder in data.get('filings', {}).get('recent', {}).get('holderOf', []):
                insider = {
                    'name': holder.get('nameOfHolder', ''),
                    'title': holder.get('title', ''),
                    'cik': holder.get('cik', ''),
                    'is_director': holder.get('isDirector', False),
                    'is_officer': holder.get('isOfficer', False),
                    'officer_title': holder.get('officerTitle', '')
                }
                insiders.append(insider)

        except Exception as e:
            logger.error(f"Error parsing insiders: {e}")

        return insiders

    def _extract_transactions(self, root) -> List[Dict]:
        """Extract transaction details from SEC filing XML"""
        transactions = []

        # SEC uses XML namespaces
        namespaces = {
            'ns': 'http://www.sec.gov/edgar/document'
        }

        # Find all transaction entries
        for transaction in root.findall('.//ns:nonDerivativeTransaction', namespaces):
            try:
                transaction_data = {
                    'transaction_type': transaction.find('ns:transactionCoding/ns:transactionCode', namespaces).text,
                    'shares': float(transaction.find('ns:transactionAmounts/ns:transactionShares/ns:value', namespaces).text),
                    'price_per_share': float(transaction.find('ns:transactionAmounts/ns:transactionPricePerShare/ns:value', namespaces).text or 0),
                    'transaction_date': transaction.find('ns:transactionDate/ns:value', namespaces).text,
                    'shares_owned_after': float(transaction.find('ns:postTransactionAmounts/ns:sharesOwnedFollowingTransaction/ns:value', namespaces).text)
                }
                transactions.append(transaction_data)

            except Exception as e:
                logger.error(f"Error extracting transaction: {e}")
                continue

        return transactions

    def save_to_queue(self, filing_data: Dict, queue_name: str = 'sec_filings'):
        """Save filing data to Redis queue for processing"""
        try:
            self.redis_client.lpush(queue_name, json.dumps(filing_data))
            logger.info(f"Saved filing to queue: {filing_data.get('accession_number')}")
        except Exception as e:
            logger.error(f"Error saving to queue: {e}")

    def run(self, interval: int = 300):
        """
        Run the scraper continuously

        Args:
            interval: Polling interval in seconds (default: 5 minutes)
        """
        logger.info(f"Starting SEC scraper, polling every {interval} seconds")

        while True:
            try:
                # Get recent Form 4 filings (most common for insider trading)
                filings = self.get_recent_filings(filing_type='4', days_back=1)

                for filing in filings:
                    # Parse each filing
                    filing_data = self.parse_filing_xml(filing['accession_number'])

                    if filing_data:
                        # Save to queue for processing
                        self.save_to_queue(filing_data)

                logger.info(f"Processed {len(filings)} filings, sleeping for {interval} seconds")
                time.sleep(interval)

            except KeyboardInterrupt:
                logger.info("Scraper stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in scraper loop: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    scraper = SECScraper()
    scraper.run()
```

#### 2. Data Processor Service (Node.js)

`backend/services/dataProcessor.js`:

```javascript
import { logger } from '../utils/logger.js';
import { saveFiling, saveTransaction, updateInsider } from '../models/Transaction.js';
import { queue } from '../workers/queue.js';

/**
 * Process SEC filing data
 */
export class DataProcessor {
  constructor() {
    this.processedCount = 0;
    this.errorCount = 0;
  }

  /**
   * Process filing from queue
   */
  async processFiling(filingData) {
    try {
      logger.info(`Processing filing: ${filingData.accession_number}`);

      // Extract insider information
      const insiderInfo = this.extractInsiderInfo(filingData);

      // Extract company information
      const companyInfo = this.extractCompanyInfo(filingData);

      // Process each transaction
      const transactions = filingData.transactions || [];

      for (const transaction of transactions) {
        await this.processTransaction(
          transaction,
          insiderInfo,
          companyInfo,
          filingData
        );
      }

      this.processedCount++;
      logger.info(`Successfully processed filing: ${filingData.accession_number}`);

    } catch (error) {
      this.errorCount++;
      logger.error(`Error processing filing: ${error.message}`, error);
      throw error;
    }
  }

  /**
   * Process individual transaction
   */
  async processTransaction(transaction, insiderInfo, companyInfo, filingData) {
    try {
      // Normalize transaction type
      const transactionType = this.normalizeTransactionType(transaction.transaction_type);

      // Calculate total value
      const totalValue = transaction.shares * transaction.price_per_share;

      // Check if transaction meets minimum threshold (e.g., $10,000)
      if (totalValue < 10000) {
        logger.debug(`Transaction below threshold: $${totalValue}`);
        return;
      }

      // Save to database
      const transactionData = {
        insider_id: insiderInfo.id,
        company_id: companyInfo.id,
        filing_type: filingData.filing_type || '4',
        transaction_date: transaction.transaction_date,
        transaction_type: transactionType,
        shares_traded: transaction.shares,
        price_per_share: transaction.price_per_share,
        total_value: totalValue,
        shares_owned_after: transaction.shares_owned_after,
        ownership_type: 'Direct', // Simplified
        sec_file_url: filingData.sec_file_url,
        filing_date: new Date().toISOString().split('T')[0]
      };

      const savedTransaction = await saveTransaction(transactionData);

      // Update insider profile
      await updateInsider(insiderInfo.id, {
        last_transaction_date: transaction.transaction_date,
        transactions_count: insiderInfo.transactions_count + 1
      });

      // Add to filter queue
      await queue.add('filter-check', {
        transaction_id: savedTransaction.id,
        transaction_data: transactionData,
        insider_info: insiderInfo,
        company_info: companyInfo
      });

      logger.info(`Transaction processed: ${transactionType} ${transaction.shares} shares of ${companyInfo.ticker}`);

    } catch (error) {
      logger.error(`Error processing transaction: ${error.message}`, error);
      throw error;
    }
  }

  /**
   * Extract insider information from filing
   */
  extractInsiderInfo(filingData) {
    // Parse filing data to extract insider info
    // This would typically query the database or parse from filing
    return {
      id: filingData.insider_id,
      name: filingData.insider_name,
      title: filingData.insider_title,
      cik: filingData.insider_cik,
      transactions_count: 0
    };
  }

  /**
   * Extract company information from filing
   */
  extractCompanyInfo(filingData) {
    // Parse filing data to extract company info
    return {
      id: filingData.company_id,
      ticker: filingData.ticker,
      company_name: filingData.company_name,
      cik: filingData.company_cik
    };
  }

  /**
   * Normalize SEC transaction codes
   */
  normalizeTransactionType(secCode) {
    const typeMap = {
      'P': 'Buy - Open market or private purchase',
      'S': 'Sell - Open market or private sale',
      'M': 'Buy - Option exercise',
      'A': 'Grant or award',
      'D': 'Sell - Disposition',
      'G': 'Gift',
      'F': 'Payment of exercise price'
    };

    return typeMap[secCode] || secCode;
  }
}

export default new DataProcessor();
```

#### 3. Filter Engine

`backend/services/filterEngine.js`:

```javascript
import { logger } from '../utils/logger.js';
import { getUserFilters } from '../models/UserFilter.js';
import { alertService } from './alertService.js';

/**
 * Filter Engine - Matches transactions against user filters
 */
export class FilterEngine {
  /**
   * Check if transaction matches any user filters
   */
  async checkFilters(transactionData, insiderInfo, companyInfo) {
    try {
      // Get all active user filters
      const filters = await getUserFilters({ is_active: true });

      logger.info(`Checking transaction against ${filters.length} filters`);

      const matchedFilters = [];

      for (const filter of filters) {
        const isMatch = await this.evaluateFilter(
          filter,
          transactionData,
          insiderInfo,
          companyInfo
        );

        if (isMatch) {
          matchedFilters.push(filter);
        }
      }

      // Send alerts for matched filters
      if (matchedFilters.length > 0) {
        for (const filter of matchedFilters) {
          await alertService.sendAlert(filter, {
            transaction: transactionData,
            insider: insiderInfo,
            company: companyInfo
          });
        }

        logger.info(`Transaction matched ${matchedFilters.length} filters, alerts sent`);
      }

      return matchedFilters;

    } catch (error) {
      logger.error(`Error checking filters: ${error.message}`, error);
      throw error;
    }
  }

  /**
   * Evaluate if transaction matches a single filter
   */
  async evaluateFilter(filter, transaction, insider, company) {
    try {
      // Check insider title filter
      if (filter.insider_titles && filter.insider_titles.length > 0) {
        const titleMatch = filter.insider_titles.some(
          title => insider.title.toLowerCase().includes(title.toLowerCase())
        );
        if (!titleMatch) return false;
      }

      // Check transaction type filter
      if (filter.transaction_types && filter.transaction_types.length > 0) {
        const typeMatch = filter.transaction_types.some(
          type => transaction.transaction_type.toLowerCase().includes(type.toLowerCase())
        );
        if (!typeMatch) return false;
      }

      // Check minimum value filter
      if (filter.min_transaction_value) {
        if (transaction.total_value < filter.min_transaction_value) {
          return false;
        }
      }

      // Check company filter
      if (filter.companies && filter.companies.length > 0) {
        const companyMatch = filter.companies.includes(company.ticker);
        if (!companyMatch) return false;
      }

      // All conditions passed
      return true;

    } catch (error) {
      logger.error(`Error evaluating filter: ${error.message}`, error);
      return false;
    }
  }

  /**
   * Score transaction relevance (for future ML implementation)
   */
  scoreTransaction(transaction, insider, company) {
    let score = 0;

    // CEO/CFO transactions are more significant
    if (insider.title && ['CEO', 'CFO', 'CTO'].includes(insider.title.toUpperCase())) {
      score += 30;
    }

    // Large transactions are more significant
    if (transaction.total_value > 1000000) {
      score += 25;
    } else if (transaction.total_value > 500000) {
      score += 20;
    } else if (transaction.total_value > 100000) {
      score += 15;
    }

    // Buy transactions may be more significant than sells
    if (transaction.transaction_type.includes('Buy')) {
      score += 10;
    }

    // First-time insider transactions
    if (insider.transactions_count === 1) {
      score += 5;
    }

    return Math.min(score, 100); // Max score of 100
  }
}

export default new FilterEngine();
```

---

## n8n Workflow Integration

### Workflow 1: SEC Filing Processor

`n8n-workflows/sec-webhook.json`:

```json
{
  "name": "SEC Filing Processor",
  "nodes": [
    {
      "name": "Webhook Receiver",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "path": "sec-filing",
        "method": "POST",
        "responseMode": "lastNode"
      }
    },
    {
      "name": "Parse Filing Data",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "values": {
          "string": [
            {
              "name": "accession_number",
              "value": "={{ $json.body.accession_number }}"
            },
            {
              "name": "company_ticker",
              "value": "={{ $json.body.company_ticker }}"
            },
            {
              "name": "insider_name",
              "value": "={{ $json.body.insider_name }}"
            },
            {
              "name": "transaction_type",
              "value": "={{ $json.body.transaction_type }}"
            },
            {
              "name": "shares",
              "value": "={{ $json.body.shares }}"
            },
            {
              "name": "price",
              "value": "={{ $json.body.price }}"
            }
          ]
        }
      }
    },
    {
      "name": "Calculate Total Value",
      "type": "n8n-nodes-base.code",
      "position": [650, 300],
      "parameters": {
        "code": "// Calculate total transaction value\nconst shares = $node[\"Parse Filing Data\"].json[\"shares\"];\nconst price = $node[\"Parse Filing Data\"].json[\"price\"];\nconst totalValue = shares * price;\n\nreturn {\n  json: {\n    ...$node[\"Parse Filing Data\"].json,\n    total_value: totalValue\n  }\n};"
      }
    },
    {
      "name": "Filter by Value",
      "type": "n8n-nodes-base.filter",
      "position": [850, 300],
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.total_value }}",
              "operation": "larger",
              "value2": "10000"
            }
          ]
        }
      }
    },
    {
      "name": "Save to Database",
      "type": "n8n-nodes-base.postgres",
      "position": [1050, 300],
      "parameters": {
        "operation": "insert",
        "table": "transactions",
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "insider_id": "={{ $json.insider_id }}",
            "company_id": "={{ $json.company_id }}",
            "transaction_type": "={{ $json.transaction_type }}",
            "shares_traded": "={{ $json.shares }}",
            "price_per_share": "={{ $json.price }}",
            "total_value": "={{ $json.total_value }}"
          }
        }
      }
    },
    {
      "name": "Send to Queue",
      "type": "n8n-nodes-base.redis",
      "position": [1250, 300],
      "parameters": {
        "operation": "push",
        "listName": "transaction_queue",
        "value": "={{ JSON.stringify($json) }}"
      }
    }
  ],
  "connections": {
    "Webhook Receiver": {
      "main": [[{ "node": "Parse Filing Data", "type": "main", "index": 0 }]]
    },
    "Parse Filing Data": {
      "main": [[{ "node": "Calculate Total Value", "type": "main", "index": 0 }]]
    },
    "Calculate Total Value": {
      "main": [[{ "node": "Filter by Value", "type": "main", "index": 0 }]]
    },
    "Filter by Value": {
      "main": [[{ "node": "Save to Database", "type": "main", "index": 0 }]]
    },
    "Save to Database": {
      "main": [[{ "node": "Send to Queue", "type": "main", "index": 0 }]]
    }
  }
}
```

### Workflow 2: Telegram Alert Sender

`n8n-workflows/notification-workflow.json`:

```json
{
  "name": "Telegram Alert Sender",
  "nodes": [
    {
      "name": "Redis Queue Consumer",
      "type": "n8n-nodes-base.redis",
      "position": [250, 300],
      "parameters": {
        "operation": "pop",
        "listName": "alert_queue"
      }
    },
    {
      "name": "Format Telegram Message",
      "type": "n8n-nodes-base.code",
      "position": [450, 300],
      "parameters": {
        "code": "// Format insider trading alert for Telegram\nconst data = $json;\n\nconst emoji = data.transaction_type.includes('Buy') ? '🟢' : '🔴';\nconst action = data.transaction_type.includes('Buy') ? 'BUY' : 'SELL';\n\nconst message = `\n${emoji} INSIDER TRADING ALERT\n\n🏢 ${data.company_name} (${data.company_ticker})\n👤 ${data.insider_name} - ${data.insider_title}\n📊 ${action} ${data.shares_traded.toLocaleString()} shares\n💰 $${data.total_value.toLocaleString()}\n💵 Price: $${data.price_per_share.toFixed(2)}\n📅 ${data.transaction_date}\n🔗 View Filing: ${data.sec_file_url}\n⏰ ${new Date().toLocaleString()}\n`;\n\nreturn {\n  json: {\n    message: message,\n    chat_id: data.user_id\n  }\n};"
      }
    },
    {
      "name": "Send Telegram Message",
      "type": "n8n-nodes-base.telegram",
      "position": [650, 300],
      "parameters": {
        "chatId": "={{ $json.chat_id }}",
        "text": "={{ $json.message }}"
      }
    },
    {
      "name": "Log Alert",
      "type": "n8n-nodes-base.postgres",
      "position": [850, 300],
      "parameters": {
        "operation": "insert",
        "table": "alert_history",
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "user_id": "={{ $json.chat_id }}",
            "transaction_id": "={{ $json.transaction_id }}",
            "alert_type": "telegram",
            "status": "sent",
            "sent_at": "={{ new Date().toISOString() }}"
          }
        }
      }
    }
  ],
  "connections": {
    "Redis Queue Consumer": {
      "main": [[{ "node": "Format Telegram Message", "type": "main", "index": 0 }]]
    },
    "Format Telegram Message": {
      "main": [[{ "node": "Send Telegram Message", "type": "main", "index": 0 }]]
    },
    "Send Telegram Message": {
      "main": [[{ "node": "Log Alert", "type": "main", "index": 0 }]]
    }
  }
}
```

---

## Frontend Dashboard

### Dashboard Features

1. **Activity Feed** - Real-time insider trading activity
2. **Insider Rankings** - Most active insiders
3. **Company Profiles** - View insider activity by company
4. **Filter Management** - Create/edit user filters
5. **Alert History** - View past notifications
6. **Statistics** - Win rates, trends, patterns
7. **Search** - Search by insider, company, ticker

### React Component Example

`frontend/src/components/InsiderActivityFeed.js`:

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const InsiderActivityFeed = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    transactionType: 'all',
    minValue: 0,
    timeRange: '24h'
  });

  useEffect(() => {
    fetchTransactions();

    // Set up WebSocket for real-time updates
    const ws = new WebSocket('ws://localhost:3000');
    ws.onmessage = (event) => {
      const newTransaction = JSON.parse(event.data);
      setTransactions(prev => [newTransaction, ...prev]);
    };

    return () => ws.close();
  }, []);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/transactions', {
        params: filters
      });
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  return (
    <div className="activity-feed">
      <h2>Insider Trading Activity</h2>

      <div className="filters">
        <select
          value={filters.transactionType}
          onChange={(e) => setFilters({...filters, transactionType: e.target.value})}
        >
          <option value="all">All Transactions</option>
          <option value="buy">Buys Only</option>
          <option value="sell">Sells Only</option>
        </select>

        <input
          type="number"
          placeholder="Min Value ($)"
          value={filters.minValue}
          onChange={(e) => setFilters({...filters, minValue: e.target.value})}
        />

        <button onClick={fetchTransactions}>Apply Filters</button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="transactions-list">
          {transactions.map(transaction => (
            <div key={transaction.id} className="transaction-card">
              <div className="transaction-header">
                <h3>{transaction.company_name} ({transaction.ticker})</h3>
                <span className={`type ${transaction.transaction_type.toLowerCase()}`}>
                  {transaction.transaction_type}
                </span>
              </div>

              <div className="transaction-details">
                <p><strong>Insider:</strong> {transaction.insider_name} - {transaction.insider_title}</p>
                <p><strong>Shares:</strong> {transaction.shares_traded.toLocaleString()}</p>
                <p><strong>Value:</strong> {formatCurrency(transaction.total_value)}</p>
                <p><strong>Date:</strong> {new Date(transaction.transaction_date).toLocaleDateString()}</p>
              </div>

              <a href={transaction.sec_file_url} target="_blank" rel="noopener noreferrer">
                View SEC Filing
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default InsiderActivityFeed;
```

---

## Deployment Options

### Option 1: Hostinger VPS (Docker Compose)

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: insider-postgres
    environment:
      POSTGRES_USER: insider_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: insider_tracking
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    container_name: insider-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Node.js Backend
  backend:
    build: .
    container_name: insider-backend
    environment:
      NODE_ENV: production
      PORT: 3000
      DATABASE_URL: postgresql://insider_user:${DB_PASSWORD}@postgres:5432/insider_tracking
      REDIS_URL: redis://redis:6379
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
    depends_on:
      - postgres
      - redis
    ports:
      - "3000:3000"
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # Python SEC Scraper
  scraper:
    build: ./scrapers
    container_name: insider-scraper
    environment:
      REDIS_HOST: redis
      REDIS_PORT: 6379
      PYTHONUNBUFFERED: 1
    depends_on:
      - redis
    volumes:
      - ./scrapers/logs:/app/logs
    restart: unless-stopped

  # n8n Workflow Automation
  n8n:
    image: n8nio/n8n:latest
    container_name: insider-n8n
    environment:
      N8N_BASIC_AUTH_ACTIVE: "true"
      N8N_BASIC_AUTH_USER: ${N8N_USER}
      N8N_BASIC_AUTH_PASSWORD: ${N8N_PASSWORD}
      WEBHOOK_URL: https://your-domain.com
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n-workflows:/workflows
    restart: unless-stopped

  # Nginx Reverse Proxy (Optional)
  nginx:
    image: nginx:alpine
    container_name: insider-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  n8n_data:
```

### Option 2: Railway.app (Simple Cloud Deploy)

1. **Backend** - Node.js service
2. **PostgreSQL** - Managed database
3. **Redis** - Upstash Redis (free tier)
4. **Workers** - Railway Cron jobs for scraper
5. **n8n** - Railway n8n template

**Cost**: ~$20-30/month

### Option 3: AWS Infrastructure

```
┌─────────────────────────────────────┐
│  AWS CloudWatch                     │
│  - Logging                          │
│  - Alarms                           │
│  - Metrics                          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  AWS Lambda                         │
│  - SEC Scraper (Python)             │
│  - Scheduled by EventBridge          │
│  - S3 for raw filings storage       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  AWS ECS Fargate                    │
│  - Node.js backend                  │
│  - Auto-scaling                     │
│  - Load balanced                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Amazon RDS PostgreSQL              │
│  - Multi-AZ                         │
│  - Automated backups                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Amazon ElastiCache Redis           │
│  - Cluster mode                     │
│  - Automatic failover               │
└─────────────────────────────────────┘
```

**Cost**: ~$100-200/month (production)

---

## Code Examples

### Complete Backend API Routes

`backend/routes/api.js`:

```javascript
import express from 'express';
import {
  getTransactions,
  getTransactionById,
  getTransactionsByInsider,
  getTransactionsByCompany,
  getStatistics
} from '../models/Transaction.js';
import {
  getUserFilters,
  createUserFilter,
  updateUserFilter,
  deleteUserFilter
} from '../models/UserFilter.js';
import { getInsiderRankings } from '../models/Insider.js';
import { logger } from '../utils/logger.js';

const router = express.Router();

/**
 * GET /api/transactions
 * Get all transactions with optional filters
 */
router.get('/transactions', async (req, res) => {
  try {
    const {
      page = 1,
      limit = 50,
      insider_id,
      company_id,
      transaction_type,
      min_value,
      start_date,
      end_date
    } = req.query;

    const filters = {
      insider_id,
      company_id,
      transaction_type,
      min_value,
      start_date,
      end_date
    };

    const result = await getTransactions(page, limit, filters);

    res.json({
      success: true,
      data: result.transactions,
      pagination: result.pagination
    });

  } catch (error) {
    logger.error('Error fetching transactions:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/transactions/:id
 * Get transaction by ID
 */
router.get('/transactions/:id', async (req, res) => {
  try {
    const transaction = await getTransactionById(req.params.id);

    if (!transaction) {
      return res.status(404).json({
        success: false,
        error: 'Transaction not found'
      });
    }

    res.json({
      success: true,
      data: transaction
    });

  } catch (error) {
    logger.error('Error fetching transaction:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/insiders/rankings
 * Get insider rankings by activity
 */
router.get('/insiders/rankings', async (req, res) => {
  try {
    const { limit = 10, period = '30d' } = req.query;

    const rankings = await getInsiderRankings(limit, period);

    res.json({
      success: true,
      data: rankings
    });

  } catch (error) {
    logger.error('Error fetching insider rankings:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/statistics
 * Get insider trading statistics
 */
router.get('/statistics', async (req, res) => {
  try {
    const { period = '30d' } = req.query;

    const stats = await getStatistics(period);

    res.json({
      success: true,
      data: stats
    });

  } catch (error) {
    logger.error('Error fetching statistics:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/filters
 * Get user filters
 */
router.get('/filters', async (req, res) => {
  try {
    const { user_id } = req.query;

    if (!user_id) {
      return res.status(400).json({
        success: false,
        error: 'user_id is required'
      });
    }

    const filters = await getUserFilters({ user_id });

    res.json({
      success: true,
      data: filters
    });

  } catch (error) {
    logger.error('Error fetching filters:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/filters
 * Create new user filter
 */
router.post('/filters', async (req, res) => {
  try {
    const filterData = req.body;

    // Validate required fields
    if (!filterData.user_id || !filterData.filter_name) {
      return res.status(400).json({
        success: false,
        error: 'user_id and filter_name are required'
      });
    }

    const filter = await createUserFilter(filterData);

    res.status(201).json({
      success: true,
      data: filter
    });

  } catch (error) {
    logger.error('Error creating filter:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * PUT /api/filters/:id
 * Update user filter
 */
router.put('/filters/:id', async (req, res) => {
  try {
    const filter = await updateUserFilter(req.params.id, req.body);

    res.json({
      success: true,
      data: filter
    });

  } catch (error) {
    logger.error('Error updating filter:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * DELETE /api/filters/:id
 * Delete user filter
 */
router.delete('/filters/:id', async (req, res) => {
  try {
    await deleteUserFilter(req.params.id);

    res.json({
      success: true,
      message: 'Filter deleted successfully'
    });

  } catch (error) {
    logger.error('Error deleting filter:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
```

---

## Best Practices

### 1. SEC API Compliance

- **Rate Limiting**: SEC allows 10 requests per second
- **User-Agent**: Required in all requests
- **CIK Formatting**: Must be 10 digits (pad with zeros)
- **Incremental Updates**: Only fetch new filings since last check
- **Error Handling**: Retry with exponential backoff

### 2. Data Processing

- **Async Processing**: Use message queues for non-blocking operations
- **Batch Processing**: Process multiple filings in batches
- **Deduplication**: Check for existing filings before processing
- **Validation**: Validate all data before storing
- **Error Recovery**: Log errors and implement retry logic

### 3. Database Optimization

- **Indexes**: Create indexes on frequently queried columns
- **Partitioning**: Partition tables by date for large datasets
- **Connection Pooling**: Use connection pooling (PgBouncer)
- **Query Optimization**: Use EXPLAIN ANALYZE for slow queries
- **Backup Strategy**: Automated daily backups with retention policy

### 4. Alert Management

- **Throttling**: Limit alerts per user per hour
- **Deduplication**: Don't send duplicate alerts for same filing
- **Priority Scoring**: Score transactions by relevance
- **User Preferences**: Allow users to customize alert frequency
- **Alert History**: Track all sent alerts for analytics

### 5. Security

- **Input Validation**: Validate all user inputs
- **Rate Limiting**: Protect API endpoints from abuse
- **Authentication**: Implement API key or OAuth authentication
- **Encryption**: Encrypt sensitive data at rest
- **Audit Logging**: Log all data access and modifications

### 6. Monitoring

- **Health Checks**: Implement /health endpoint
- **Metrics**: Track application metrics (Prometheus/Grafana)
- **Logging**: Structured logging with correlation IDs
- **Alerting**: Alert on errors, high latency, or downtime
- **Performance**: Monitor database query performance

### 7. Testing

- **Unit Tests**: Test all business logic
- **Integration Tests**: Test database operations
- **Load Tests**: Test system under high load
- **Mock SEC API**: Use mock data for development
- **CI/CD**: Automated testing in deployment pipeline

---

## Cost Breakdown

### Hostinger VPS (Recommended)

```
VPS: ~$8-15/month
Domain: ~$10/year
SSL Certificate: Free (Let's Encrypt)

Total: ~$120-180/year
```

### Railway.app (Cloud)

```
Backend: $5-20/month
PostgreSQL: $5-20/month
Redis (Upstash): Free tier
n8n: $0-20/month (community edition)

Total: ~$10-60/month
```

### AWS (Production)

```
EC2/ECS: $30-100/month
RDS PostgreSQL: $50-200/month
ElastiCache Redis: $25-100/month
Lambda: $0-20/month
S3: $0-5/month
CloudWatch: $0-10/month

Total: ~$100-400/month
```

---

## Quick Start Guide

### 1. Clone and Setup

```bash
git clone https://github.com/your-repo/insider-tracking.git
cd insider-tracking

# Copy environment file
cp config/.env.example .env

# Edit .env with your credentials
nano .env
```

### 2. Start with Docker

```bash
# Start all services
docker-compose up -d

# Initialize database
docker-compose exec postgres psql -U insider_user -d insider_tracking -f /docker-entrypoint-initdb.d/init.sql

# Run migrations
docker-compose exec backend npm run migrate

# Check logs
docker-compose logs -f
```

### 3. Access Services

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:3000/api
- **n8n**: http://localhost:5678
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 4. Configure Telegram Bot

```bash
# Create bot via @BotFather
# Get token and add to .env

# Get chat ID via @userinfobot
# Add to .env

# Test notification
curl -X POST http://localhost:3000/api/test-notification
```

---

## Conclusion

This architecture provides a **production-ready, scalable solution** for tracking insider trading activity. The system is designed to:

- **Monitor SEC filings** in real-time
- **Process data efficiently** using message queues
- **Filter based on user criteria**
- **Send notifications** via Telegram
- **Provide insights** through a dashboard
- **Scale horizontally** as data volume grows
- **Deploy easily** on VPS or cloud platforms

The modular design allows you to start simple and add features as needed. The total cost can be as low as **$120-180/year** on Hostinger VPS, making it accessible for individual traders and small firms.

---

## Next Steps

1. **Set up development environment**
2. **Create PostgreSQL database**
3. **Implement SEC scraper** (Python)
4. **Build data processor** (Node.js)
5. **Create filter engine**
6. **Implement Telegram alerts**
7. **Build dashboard UI**
8. **Deploy to production**
9. **Monitor and optimize**
10. **Iterate based on feedback**

---

**Author**: Claude Code
**Last Updated**: February 2025
**Version**: 1.0.0
