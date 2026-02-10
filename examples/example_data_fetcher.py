"""
Example: Simple Data Fetcher using yfinance
This module demonstrates how to fetch historical stock data.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


class DataFetcher:
    """
    Fetches historical market data using Yahoo Finance API.
    
    Example usage:
        fetcher = DataFetcher()
        data = fetcher.fetch_historical_data('SPY', '2023-01-01', '2024-01-01')
        print(data.head())
    """
    
    def __init__(self):
        """Initialize the data fetcher."""
        pass
    
    def fetch_historical_data(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str, 
        interval: str = '1d'
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical OHLCV data for a given symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'SPY', 'AAPL')
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            interval: Data interval ('1d', '1h', '5m', etc.)
        
        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume
            Returns None if data fetch fails
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            if data.empty:
                print(f"No data found for {symbol}")
                return None
            
            # Rename columns to lowercase for consistency
            data.columns = [col.lower() for col in data.columns]
            
            return data
        
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def fetch_latest_data(self, symbol: str, period: str = '1mo') -> Optional[pd.DataFrame]:
        """
        Fetch recent data for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period ('1d', '5d', '1mo', '3mo', '1y', etc.)
        
        Returns:
            DataFrame with recent OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                print(f"No data found for {symbol}")
                return None
            
            data.columns = [col.lower() for col in data.columns]
            return data
        
        except Exception as e:
            print(f"Error fetching latest data for {symbol}: {e}")
            return None


def main():
    """Example usage of DataFetcher."""
    print("=== Data Fetcher Example ===\n")
    
    fetcher = DataFetcher()
    
    # Example 1: Fetch historical data for SPY
    print("Fetching SPY data for 2023...")
    spy_data = fetcher.fetch_historical_data('SPY', '2023-01-01', '2023-12-31')
    
    if spy_data is not None:
        print(f"Fetched {len(spy_data)} rows of data")
        print("\nFirst 5 rows:")
        print(spy_data.head())
        print("\nBasic statistics:")
        print(spy_data['close'].describe())
    
    # Example 2: Fetch latest data
    print("\n" + "="*50)
    print("Fetching latest 1 month data for AAPL...")
    aapl_data = fetcher.fetch_latest_data('AAPL', period='1mo')
    
    if aapl_data is not None:
        print(f"Fetched {len(aapl_data)} rows of recent data")
        print("\nLast 5 rows:")
        print(aapl_data.tail())


if __name__ == "__main__":
    main()
