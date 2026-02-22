"""
Demo data generator for testing the trading bot without Binance API access.
Generates realistic BTC/USDT price data for testing purposes.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DemoDataGenerator:
    """
    Generate demo OHLCV data for testing.
    """
    
    @staticmethod
    def generate_demo_data(start_price: float = 50000.0, 
                          num_candles: int = 2160,  # 90 days of 1-hour candles
                          volatility: float = 0.02) -> pd.DataFrame:
        """
        Generate realistic demo OHLCV data with trend and volatility.
        
        Args:
            start_price: Starting price
            num_candles: Number of candles to generate
            volatility: Price volatility (default: 2%)
            
        Returns:
            DataFrame with OHLCV data
        """
        np.random.seed(42)  # For reproducibility
        
        timestamps = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []
        
        current_time = datetime.now() - timedelta(hours=num_candles)
        current_price = start_price
        
        # Add some trend components
        trend_period = 200
        trend_strength = 0.0005
        
        for i in range(num_candles):
            # Add trend component (sine wave)
            trend = np.sin(2 * np.pi * i / trend_period) * trend_strength
            
            # Random walk with trend
            price_change = np.random.randn() * volatility + trend
            current_price = current_price * (1 + price_change)
            
            # Generate OHLC for this candle
            open_price = current_price
            close_price = current_price * (1 + np.random.randn() * volatility)
            
            high_price = max(open_price, close_price) * (1 + abs(np.random.randn()) * volatility * 0.5)
            low_price = min(open_price, close_price) * (1 - abs(np.random.randn()) * volatility * 0.5)
            
            volume = np.random.uniform(100, 1000)
            
            timestamps.append(current_time)
            opens.append(open_price)
            highs.append(high_price)
            lows.append(low_price)
            closes.append(close_price)
            volumes.append(volume)
            
            current_time += timedelta(hours=1)
            current_price = close_price
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes
        })
        
        return df
    
    @staticmethod
    def save_demo_data(filepath: str, **kwargs):
        """
        Generate and save demo data to CSV.
        
        Args:
            filepath: Path to save CSV file
            **kwargs: Arguments passed to generate_demo_data
        """
        df = DemoDataGenerator.generate_demo_data(**kwargs)
        df.to_csv(filepath, index=False)
        print(f"Demo data saved to {filepath}")
    
    @staticmethod
    def load_demo_data(filepath: str) -> pd.DataFrame:
        """
        Load demo data from CSV.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with OHLCV data
        """
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
