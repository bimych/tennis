"""
Technical indicators module for calculating EMA and other indicators.
"""
import pandas as pd
import numpy as np
from typing import Tuple


class Indicators:
    """
    Calculate technical indicators for trading strategy.
    """
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA).
        
        Args:
            data: Price data series
            period: EMA period
            
        Returns:
            EMA values as pandas Series
        """
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def add_emas(df: pd.DataFrame, short_period: int = 20, long_period: int = 50) -> pd.DataFrame:
        """
        Add EMA columns to dataframe.
        
        Args:
            df: DataFrame with 'close' column
            short_period: Short EMA period (default: 20)
            long_period: Long EMA period (default: 50)
            
        Returns:
            DataFrame with added EMA columns
        """
        df = df.copy()
        df['ema_short'] = Indicators.calculate_ema(df['close'], short_period)
        df['ema_long'] = Indicators.calculate_ema(df['close'], long_period)
        return df
    
    @staticmethod
    def find_swing_low(df: pd.DataFrame, lookback: int = 10) -> float:
        """
        Find the recent swing low in price data.
        
        Args:
            df: DataFrame with 'low' column
            lookback: Number of candles to look back
            
        Returns:
            Swing low price
        """
        if len(df) < lookback:
            lookback = len(df)
        return df['low'].iloc[-lookback:].min()
    
    @staticmethod
    def is_uptrend(ema_short: float, ema_long: float) -> bool:
        """
        Check if market is in uptrend (EMA short > EMA long).
        
        Args:
            ema_short: Short EMA value
            ema_long: Long EMA value
            
        Returns:
            True if uptrend, False otherwise
        """
        return ema_short > ema_long
    
    @staticmethod
    def is_price_near_ema(price: float, ema: float, tolerance: float = 0.01) -> bool:
        """
        Check if price is within tolerance% of EMA.
        
        Args:
            price: Current price
            ema: EMA value
            tolerance: Tolerance percentage (default: 0.01 for 1%)
            
        Returns:
            True if price is within tolerance, False otherwise
        """
        upper_bound = ema * (1 + tolerance)
        lower_bound = ema * (1 - tolerance)
        return lower_bound <= price <= upper_bound
