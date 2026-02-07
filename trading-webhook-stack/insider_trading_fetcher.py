#!/usr/bin/env python3
"""
Insider Trading Data Fetcher
Fetches SEC Form 4 insider trading data for US stocks

Usage:
    python insider_trading_fetcher.py --ticker AAPL
    python insider_trading_fetcher.py --ticker AAPL --days 30
    python insider_trading_fetcher.py --tickers AAPL,MSFT,GOOGL
    python insider_trading_fetcher.py --signals --days 7
"""

import requests
import argparse
import pandas as pd
from datetime import datetime, timedelta
import time
import xml.etree.ElementTree as ET
import json
from typing import List, Dict, Optional


class SECInsiderTrading:
    """Fetch SEC Form 4 insider trading data"""

    BASE_URL = "https://www.sec.gov"

    def __init__(self, user_agent: str = "Your Name (your.email@example.com)"):
        self.headers = {
            'User-Agent': user_agent,
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json'
        }
        self.ticker_to_cik = {}
        self.cik_to_ticker = {}

    def load_ticker_mappings(self, force_reload: bool = False):
        """Load ticker to CIK mappings from SEC"""
        url = f"{self.BASE_URL}/files/company_tickers.json"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Build mappings
            for item in data.values():
                ticker = item['ticker'].upper()
                cik = str(item['cik_str']).zfill(10)

                self.ticker_to_cik[ticker] = cik
                self.cik_to_ticker[cik] = ticker

            print(f"✓ Loaded {len(self.ticker_to_cik)} ticker mappings")

        except Exception as e:
            print(f"✗ Error loading ticker mappings: {e}")

    def get_cik(self, ticker: str) -> Optional[str]:
        """Convert ticker to CIK"""
        ticker = ticker.upper()

        if not self.ticker_to_cik:
            self.load_ticker_mappings()

        return self.ticker_to_cik.get(ticker)

    def get_ticker(self, cik: str) -> Optional[str]:
        """Convert CIK to ticker"""
        if not self.cik_to_ticker:
            self.load_ticker_mappings()

        return self.cik_to_ticker.get(cik)

    def get_company_submissions(self, cik: str) -> Optional[Dict]:
        """Get all filings for a company"""
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"✗ Error fetching submissions for {cik}: {e}")
            return None

    def get_form4_filings(self, ticker: str, days_back: int = 30) -> pd.DataFrame:
        """Get recent Form 4 filings for a ticker"""
        cik = self.get_cik(ticker)

        if not cik:
            print(f"✗ Ticker {ticker} not found")
            return pd.DataFrame()

        print(f"Fetching filings for {ticker} (CIK: {cik})...")

        data = self.get_company_submissions(cik)
        if not data:
            return pd.DataFrame()

        # Extract filings
        filings = data['filings']['recent']

        # Get minimum length to avoid array mismatch
        min_len = min(
            len(filings['accessionNumber']),
            len(filings['filingDate']),
            len(filings['form'])
        )

        # Create DataFrame with equal length arrays
        report_dates = filings.get('periodOfReport', [])
        report_dates = report_dates[:min_len] + [None] * (min_len - len(report_dates))

        df = pd.DataFrame({
            'accession_number': filings['accessionNumber'][:min_len],
            'filing_date': filings['filingDate'][:min_len],
            'report_date': report_dates,
            'form': filings['form'][:min_len]
        })

        # Filter for Form 4
        df = df[df['form'] == '4'].copy()

        if df.empty:
            print(f"✗ No Form 4 filings found for {ticker}")
            return pd.DataFrame()

        # Convert dates
        df['filing_date'] = pd.to_datetime(df['filing_date'])

        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days_back)
        df = df[df['filing_date'] >= cutoff_date].copy()

        # Add ticker
        df['ticker'] = ticker
        df['cik'] = cik

        print(f"✓ Found {len(df)} Form 4 filings for {ticker} in last {days_back} days")

        return df[['ticker', 'cik', 'accession_number', 'filing_date', 'report_date']]

    def download_form4(self, cik: str, accession_number: str) -> Optional[str]:
        """Download full Form 4 filing text"""
        acc_clean = accession_number.replace('-', '')
        url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{acc_clean}.txt"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"✗ Error downloading Form 4: {e}")
            return None

    def parse_form4(self, filing_text: str) -> List[Dict]:
        """Parse Form 4 filing to extract transactions"""
        transactions = []

        try:
            # Find XML content
            lines = filing_text.split('\n')
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

            xml_text = '\n'.join(lines[xml_start + 1:xml_end])

            # Parse XML
            root = ET.fromstring(xml_text)

            # Namespace (if present)
            namespace = {'ns': 'http://www.sec.gov/edgar/document'} if 'http://www.sec.gov' in filing_text else {}

            # Extract reporting owner info
            reporting_owner = root.find('.//reportingOwner') or root.find('.//reportingOwnerId')

            insider_name = "Unknown"
            if reporting_owner is not None:
                name_elem = reporting_owner.find('.//reportingOwnerName') or reporting_owner.find('.//rptOwnerName')
                if name_elem is not None:
                    insider_name = name_elem.text

            # Extract position/title
            position = "Unknown"
            officer_title = root.find('.//officerTitle')
            if officer_title is not None:
                position = officer_title.text

            # Extract non-derivative transactions
            for transaction in root.findall('.//nonDerivativeTransaction'):
                try:
                    # Transaction date
                    date_elem = transaction.find('.//transactionDate/date')
                    transaction_date = date_elem.text if date_elem is not None else ""

                    # Transaction coding
                    coding = transaction.find('.//transactionCoding')
                    if coding is None:
                        continue

                    transaction_code = coding.find('.//transactionCode').text if coding.find('.//transactionCode') is not None else ""
                    transaction_type = coding.find('.//transactionTimeliness').text if coding.find('.//transactionTimeliness') is not None else ""

                    # Transaction amounts
                    amounts = transaction.find('.//transactionAmounts')
                    if amounts is None:
                        continue

                    shares_elem = amounts.find('.//transactionShares/value')
                    shares = float(shares_elem.text) if shares_elem is not None and shares_elem.text else 0

                    price_elem = amounts.find('.//transactionPricePerShare/value')
                    price = float(price_elem.text) if price_elem is not None and price_elem.text else 0

                    # Calculate total value
                    total_value = shares * price

                    # Post-transaction amounts
                    post_amounts = transaction.find('.//postTransactionAmounts')
                    shares_owned = 0
                    if post_amounts is not None:
                        shares_owned_elem = post_amounts.find('.//sharesOwnedFollowingTransaction/value')
                        if shares_owned_elem is not None and shares_owned_elem.text:
                            shares_owned = float(shares_owned_elem.text)

                    transactions.append({
                        'insider_name': insider_name,
                        'position': position,
                        'transaction_date': transaction_date,
                        'transaction_code': transaction_code,
                        'shares': shares,
                        'price_per_share': price,
                        'total_value': total_value,
                        'shares_owned_after': shares_owned
                    })

                except Exception as e:
                    print(f"✗ Error parsing transaction: {e}")
                    continue

        except Exception as e:
            print(f"✗ Error parsing Form 4 XML: {e}")

        return transactions

    def get_insider_trading(self, ticker: str, days_back: int = 30, fetch_details: bool = False) -> pd.DataFrame:
        """Get complete insider trading data for a ticker"""
        # Get filings
        filings_df = self.get_form4_filings(ticker, days_back)

        if filings_df.empty:
            return pd.DataFrame()

        if not fetch_details:
            return filings_df

        # Fetch detailed transaction data for each filing
        all_transactions = []

        for _, filing in filings_df.iterrows():
            print(f"  Downloading {filing['accession_number']}...")

            filing_text = self.download_form4(filing['cik'], filing['accession_number'])

            if filing_text:
                transactions = self.parse_form4(filing_text)

                for transaction in transactions:
                    transaction['ticker'] = ticker
                    transaction['filing_date'] = filing['filing_date']
                    transaction['accession_number'] = filing['accession_number']
                    all_transactions.append(transaction)

            # Be nice to SEC servers
            time.sleep(0.2)

        if all_transactions:
            df = pd.DataFrame(all_transactions)
            print(f"✓ Extracted {len(df)} transactions from {len(filings_df)} filings")
            return df
        else:
            return pd.DataFrame()

    def get_multiple_tickers(self, tickers: List[str], days_back: int = 30, fetch_details: bool = False) -> pd.DataFrame:
        """Fetch insider trading data for multiple tickers"""
        all_data = []

        for ticker in tickers:
            print(f"\n{'='*60}")
            print(f"Processing {ticker}...")
            print(f"{'='*60}")

            df = self.get_insider_trading(ticker, days_back, fetch_details)

            if not df.empty:
                all_data.append(df)

            # Rate limiting between tickers
            time.sleep(1)

        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            return combined
        else:
            return pd.DataFrame()


class InsiderSignalAnalyzer:
    """Analyze insider trading and generate signals"""

    TRANSACTION_CODES = {
        'P': 'Purchase',
        'S': 'Sale',
        'M': 'Multiple transactions',
        'A': 'Grant/Award',
        'D': 'Sale to issuer',
        'F': 'Payment of exercise price',
        'G': 'Gift',
        'X': 'Option exercise'
    }

    @staticmethod
    def calculate_signal(transaction: Dict) -> str:
        """
        Calculate signal strength based on transaction details

        Returns: STRONG_BUY, BUY, NEUTRAL, SELL, STRONG_SELL
        """
        score = 0

        # Transaction type scoring
        code = transaction.get('transaction_code', '')

        if code == 'P':  # Purchase
            score += 2
        elif code == 'S':  # Sale
            score -= 1
        elif code == 'A':  # Award
            score += 1  # Slightly bullish

        # Size scoring
        value = transaction.get('total_value', 0)
        if value > 1000000:  # >$1M
            score += 2
        elif value > 100000:  # >$100k
            score += 1

        # Position scoring
        position = str(transaction.get('position', '')).lower()
        if 'ceo' in position or 'chief executive' in position:
            score += 2
        elif 'cfo' in position or 'chief financial' in position:
            score += 2
        elif 'director' in position:
            score += 1

        # Determine signal
        if score >= 5:
            return 'STRONG_BUY'
        elif score >= 3:
            return 'BUY'
        elif score >= 0:
            return 'NEUTRAL'
        elif score >= -2:
            return 'SELL'
        else:
            return 'STRONG_SELL'

    @staticmethod
    def analyze_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Add signal column to DataFrame"""
        if df.empty:
            return df

        df = df.copy()
        df['signal'] = df.apply(InsiderSignalAnalyzer.calculate_signal, axis=1)
        df['transaction_type'] = df['transaction_code'].map(
            InsiderSignalAnalyzer.TRANSACTION_CODES
        ).fillna(df['transaction_code'])

        return df


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Fetch SEC Form 4 insider trading data')

    parser.add_argument('--ticker', type=str, help='Stock ticker symbol')
    parser.add_argument('--tickers', type=str, help='Comma-separated list of ticker symbols')
    parser.add_argument('--days', type=int, default=30, help='Number of days to look back (default: 30)')
    parser.add_argument('--details', action='store_true', help='Fetch detailed transaction data')
    parser.add_argument('--signals', action='store_true', help='Generate trading signals')
    parser.add_argument('--output', type=str, help='Output CSV file path')
    parser.add_argument('--user-agent', type=str, default='Your Name (your.email@example.com)',
                       help='User-Agent header for SEC requests')

    args = parser.parse_args()

    # Validate arguments
    if not args.ticker and not args.tickers:
        parser.error('Either --ticker or --tickers must be specified')

    # Determine tickers to fetch
    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(',')]
    else:
        tickers = [args.ticker.upper()]

    print(f"Fetching insider trading data for: {', '.join(tickers)}")
    print(f"Looking back {args.days} days")
    print()

    # Initialize fetcher
    sec = SECInsiderTrading(user_agent=args.user_agent)

    # Fetch data
    df = sec.get_multiple_tickers(tickers, days_back=args.days, fetch_details=args.details)

    if df.empty:
        print("\n✗ No data found")
        return

    # Generate signals if requested
    if args.signals and args.details:
        print("\n" + "="*60)
        print("Generating trading signals...")
        print("="*60)

        df = InsiderSignalAnalyzer.analyze_dataframe(df)

        # Show signal summary
        print("\nSignal Summary:")
        print(df['signal'].value_counts())

    # Display results
    print("\n" + "="*60)
    print("Results")
    print("="*60)

    if args.details:
        # Show detailed transactions
        display_cols = ['ticker', 'filing_date', 'insider_name', 'position',
                       'transaction_type', 'shares', 'total_value']

        if args.signals:
            display_cols.append('signal')

        print(df[display_cols].to_string(index=False))

        # Show summary statistics
        print("\n" + "="*60)
        print("Summary Statistics")
        print("="*60)

        for ticker in df['ticker'].unique():
            ticker_df = df[df['ticker'] == ticker]
            print(f"\n{ticker}:")
            print(f"  Total transactions: {len(ticker_df)}")
            print(f"  Total value: ${ticker_df['total_value'].sum():,.2f}")

            if args.signals:
                bullish = ticker_df[ticker_df['signal'].isin(['BUY', 'STRONG_BUY'])]
                bearish = ticker_df[ticker_df['signal'].isin(['SELL', 'STRONG_SELL'])]

                print(f"  Bullish signals: {len(bullish)}")
                print(f"  Bearish signals: {len(bearish)}")

    else:
        # Show filing summary
        print(df.to_string(index=False))

    # Save to CSV if requested
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\n✓ Data saved to {args.output}")

    print(f"\n✓ Complete!")


if __name__ == '__main__':
    main()
