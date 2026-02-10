"""
Data fetching module for retrieving historical and current market data from Binance.
"""
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from .config import BINANCE_API_KEY, BINANCE_API_SECRET, USE_TESTNET, SYMBOL, TIMEFRAME


class DataFetcher:
    """
    Fetches historical OHLCV data and current market prices from Binance.
    """
    
    def __init__(self, api_key: str = BINANCE_API_KEY, api_secret: str = BINANCE_API_SECRET, 
                 testnet: bool = USE_TESTNET):
        """
        Initialize the DataFetcher with Binance API credentials.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        self.testnet = testnet
        if testnet:
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.API_URL = 'https://testnet.binance.vision/api'
        else:
            self.client = Client(api_key, api_secret)
    
    def get_historical_data(self, symbol: str = SYMBOL, interval: str = TIMEFRAME, 
                           lookback_days: int = 90) -> pd.DataFrame:
        """
        Fetch historical OHLCV data from Binance.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            interval: Candlestick interval (e.g., '1h')
            lookback_days: Number of days to look back
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        try:
            # Calculate start time
            start_time = datetime.now() - timedelta(days=lookback_days)
            start_str = start_time.strftime("%d %b %Y %H:%M:%S")
            
            # Fetch klines from Binance
            klines = self.client.get_historical_klines(
                symbol, 
                interval, 
                start_str
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # Select and convert relevant columns
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
            
            return df
            
        except BinanceAPIException as e:
            print(f"Binance API error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            raise
    
    def get_current_price(self, symbol: str = SYMBOL) -> float:
        """
        Get the current market price for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            
        Returns:
            Current price as float
        """
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            print(f"Binance API error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching current price: {e}")
            raise
    
    def get_account_balance(self) -> dict:
        """
        Get account balance for all assets.
        
        Returns:
            Dictionary with asset balances
        """
        try:
            account = self.client.get_account()
            balances = {}
            for balance in account['balances']:
                free = float(balance['free'])
                locked = float(balance['locked'])
                if free > 0 or locked > 0:
                    balances[balance['asset']] = {
                        'free': free,
                        'locked': locked,
                        'total': free + locked
                    }
            return balances
        except BinanceAPIException as e:
            print(f"Binance API error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching account balance: {e}")
            raise
