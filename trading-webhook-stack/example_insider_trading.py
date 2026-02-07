#!/usr/bin/env python3
"""
Example: How to use Insider Trading Data Fetcher

This script demonstrates various use cases for the insider trading fetcher.
"""

from insider_trading_fetcher import SECInsiderTrading, InsiderSignalAnalyzer
import pandas as pd


def example_1_basic_fetch():
    """Example 1: Basic fetch for a single ticker"""
    print("="*70)
    print("Example 1: Basic fetch for Apple (AAPL)")
    print("="*70)

    sec = SECInsiderTrading()

    # Fetch recent Form 4 filings (no details)
    filings_df = sec.get_form4_filings('AAPL', days_back=30)

    if not filings_df.empty:
        print(f"\nFound {len(filings_df)} Form 4 filings:")
        print(filings_df[['ticker', 'filing_date', 'accession_number']].head())
    else:
        print("\nNo filings found")

    print()


def example_2_detailed_transactions():
    """Example 2: Fetch detailed transaction data"""
    print("="*70)
    print("Example 2: Detailed transactions for Tesla (TSLA)")
    print("="*70)

    sec = SECInsiderTrading()

    # Fetch detailed transaction data
    transactions_df = sec.get_insider_trading('TSLA', days_back=14, fetch_details=True)

    if not transactions_df.empty:
        print(f"\nFound {len(transactions_df)} transactions:\n")

        # Show recent purchases
        purchases = transactions_df[transactions_df['transaction_code'] == 'P']

        if not purchases.empty:
            print("Recent Purchases:")
            for _, row in purchases.head(3).iterrows():
                print(f"  {row['insider_name']} ({row['position']})")
                print(f"    {row['shares']:,.0f} shares @ ${row['price_per_share']:.2f}")
                print(f"    Total: ${row['total_value']:,.2f}")
                print(f"    Date: {row['transaction_date']}")
                print()
    else:
        print("\nNo transactions found")

    print()


def example_3_signal_analysis():
    """Example 3: Generate trading signals"""
    print("="*70)
    print("Example 3: Signal analysis for Microsoft (MSFT)")
    print("="*70)

    sec = SECInsiderTrading()

    # Fetch detailed data
    df = sec.get_insider_trading('MSFT', days_back=30, fetch_details=True)

    if not df.empty:
        # Generate signals
        df = InsiderSignalAnalyzer.analyze_dataframe(df)

        print(f"\nAnalyzed {len(df)} transactions\n")

        # Show signal distribution
        print("Signal Distribution:")
        print(df['signal'].value_counts())
        print()

        # Show strong buys
        strong_buys = df[df['signal'] == 'STRONG_BUY']
        if not strong_buys.empty:
            print("Strong Buy Signals:")
            for _, row in strong_buys.iterrows():
                print(f"  🚀 {row['insider_name']} ({row['position']})")
                print(f"     {row['transaction_type']}: {row['shares']:,.0f} shares = ${row['total_value']:,.2f}")
                print()
    else:
        print("\nNo data found")

    print()


def example_4_multiple_tickers():
    """Example 4: Batch process multiple tickers"""
    print("="*70)
    print("Example 4: Multiple tech stocks")
    print("="*70)

    sec = SECInsiderTrading()

    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

    print(f"Fetching data for: {', '.join(tickers)}\n")

    # Fetch for all tickers
    combined_df = sec.get_multiple_tickers(tickers, days_back=14, fetch_details=True)

    if not combined_df.empty:
        # Generate signals
        combined_df = InsiderSignalAnalyzer.analyze_dataframe(combined_df)

        # Summary by ticker
        print("Summary by Ticker:")
        print("-" * 70)

        for ticker in tickers:
            ticker_data = combined_df[combined_df['ticker'] == ticker]

            if not ticker_data.empty:
                total_value = ticker_data['total_value'].sum()
                bullish = len(ticker_data[ticker_data['signal'].isin(['BUY', 'STRONG_BUY'])])
                bearish = len(ticker_data[ticker_data['signal'].isin(['SELL', 'STRONG_SELL'])])

                print(f"\n{ticker}:")
                print(f"  Transactions: {len(ticker_data)}")
                print(f"  Total Value: ${total_value:,.2f}")
                print(f"  Bullish Signals: {bullish}")
                print(f"  Bearish Signals: {bearish}")
    else:
        print("\nNo data found")

    print()


def example_5_find_best_opportunities():
    """Example 5: Find stocks with strongest insider buying"""
    print("="*70)
    print("Example 5: Find best insider buying opportunities")
    print("="*70)

    sec = SECInsiderTrading()

    # Tech stocks to analyze
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'TSLA', 'AMZN']

    print(f"Analyzing {len(tickers)} stocks for insider buying...\n")

    opportunities = []

    for ticker in tickers:
        df = sec.get_insider_trading(ticker, days_back=30, fetch_details=True)

        if not df.empty:
            df = InsiderSignalAnalyzer.analyze_dataframe(df)

            # Count strong buys
            strong_buys = df[df['signal'] == 'STRONG_BUY']
            buys = df[df['signal'] == 'BUY']

            if len(strong_buys) > 0 or len(buys) > 0:
                total_buy_value = df[df['signal'].isin(['BUY', 'STRONG_BUY'])]['total_value'].sum()

                opportunities.append({
                    'ticker': ticker,
                    'strong_buys': len(strong_buys),
                    'buys': len(buys),
                    'total_buy_value': total_buy_value
                })

    # Sort by total buy value
    if opportunities:
        opportunities = sorted(opportunities, key=lambda x: x['total_buy_value'], reverse=True)

        print("Top Insider Buying Stocks:")
        print("-" * 70)

        for opp in opportunities[:5]:
            print(f"\n🚀 {opp['ticker']}")
            print(f"   Strong Buys: {opp['strong_buys']}")
            print(f"   Buys: {opp['buys']}")
            print(f"   Total Value: ${opp['total_buy_value']:,.2f}")
    else:
        print("No insider buying found in analyzed stocks")

    print()


def example_6_export_to_csv():
    """Example 6: Export data to CSV"""
    print("="*70)
    print("Example 6: Export to CSV")
    print("="*70)

    sec = SECInsiderTrading()

    # Fetch data
    df = sec.get_insider_trading('AAPL', days_back=30, fetch_details=True)

    if not df.empty:
        df = InsiderSignalAnalyzer.analyze_dataframe(df)

        # Export to CSV
        filename = 'aapl_insider_trading.csv'
        df.to_csv(filename, index=False)

        print(f"\n✓ Exported {len(df)} transactions to {filename}")
        print(f"  File size: {len(df)} rows × {len(df.columns)} columns")
    else:
        print("\nNo data to export")

    print()


def example_7_filter_executive_trades():
    """Example 7: Filter for C-level executive trades"""
    print("="*70)
    print("Example 7: C-Level Executive Trades")
    print("="*70)

    sec = SECInsiderTrading()

    df = sec.get_insider_trading('AAPL', days_back=60, fetch_details=True)

    if not df.empty:
        df = InsiderSignalAnalyzer.analyze_dataframe(df)

        # Filter for C-level executives
        c_level_filter = df['position'].str.contains('CEO|CFO|CTO|COO|Chief', case=False, na=False)
        c_level_trades = df[c_level_filter]

        if not c_level_trades.empty:
            print(f"\nFound {len(c_level_trades)} C-level transactions:\n")

            for _, row in c_level_trades.head(5).iterrows():
                signal_emoji = {
                    'STRONG_BUY': '🚀🚀🚀',
                    'BUY': '🚀',
                    'SELL': '⚠️',
                    'STRONG_SELL': '🔴🔴🔴'
                }.get(row['signal'], '➡️')

                print(f"{signal_emoji} {row['insider_name']} ({row['position']})")
                print(f"   {row['transaction_type']}: {row['shares']:,.0f} shares")
                print(f"   Value: ${row['total_value']:,.2f}")
                print(f"   Date: {row['transaction_date']}")
                print(f"   Signal: {row['signal']}")
                print()
        else:
            print("\nNo C-level trades found")
    else:
        print("\nNo data found")

    print()


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("  Insider Trading Data Fetcher - Usage Examples")
    print("="*70)
    print()

    # Run examples
    example_1_basic_fetch()
    example_2_detailed_transactions()
    example_3_signal_analysis()
    example_4_multiple_tickers()
    example_5_find_best_opportunities()
    example_6_export_to_csv()
    example_7_filter_executive_trades()

    print("="*70)
    print("All examples completed!")
    print("="*70)


if __name__ == '__main__':
    main()
