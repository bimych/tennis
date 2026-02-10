"""
Example: Simple Moving Average Crossover Strategy
This module demonstrates a basic trend-following strategy using dual moving averages.
"""

import pandas as pd
import numpy as np
from typing import Dict


class SimpleMACrossStrategy:
    """
    Simple Moving Average Crossover Strategy
    
    Strategy Logic:
    - Buy when fast MA crosses above slow MA (Golden Cross)
    - Sell when fast MA crosses below slow MA (Death Cross)
    
    This is one of the most basic trend-following strategies.
    
    Example usage:
        strategy = SimpleMACrossStrategy(fast_period=50, slow_period=200)
        signals = strategy.generate_signals(data)
    """
    
    def __init__(self, fast_period: int = 50, slow_period: int = 200):
        """
        Initialize the strategy.
        
        Args:
            fast_period: Period for fast moving average (default: 50)
            slow_period: Period for slow moving average (default: 200)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
    
    def calculate_moving_averages(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate fast and slow moving averages.
        
        Args:
            data: DataFrame with 'close' column
        
        Returns:
            DataFrame with added 'fast_ma' and 'slow_ma' columns
        """
        df = data.copy()
        df['fast_ma'] = df['close'].rolling(window=self.fast_period).mean()
        df['slow_ma'] = df['close'].rolling(window=self.slow_period).mean()
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on MA crossover.
        
        Args:
            data: DataFrame with 'close' column
        
        Returns:
            DataFrame with signals:
            - signal = 1: Buy signal (go long)
            - signal = -1: Sell signal (close long or go short)
            - signal = 0: Hold current position
        """
        df = self.calculate_moving_averages(data)
        
        # Initialize signal column
        df['signal'] = 0
        
        # Create crossover signals
        # Buy when fast MA crosses above slow MA
        df['signal'] = np.where(
            (df['fast_ma'] > df['slow_ma']) & 
            (df['fast_ma'].shift(1) <= df['slow_ma'].shift(1)), 
            1, 
            df['signal']
        )
        
        # Sell when fast MA crosses below slow MA
        df['signal'] = np.where(
            (df['fast_ma'] < df['slow_ma']) & 
            (df['fast_ma'].shift(1) >= df['slow_ma'].shift(1)), 
            -1, 
            df['signal']
        )
        
        # Create position column (1 = long, 0 = flat, -1 = short)
        df['position'] = 0
        df['position'] = np.where(df['fast_ma'] > df['slow_ma'], 1, 0)
        df['position'] = np.where(df['fast_ma'] < df['slow_ma'], -1, df['position'])
        
        return df
    
    def get_strategy_stats(self, signals_df: pd.DataFrame) -> Dict:
        """
        Calculate basic statistics about the signals.
        
        Args:
            signals_df: DataFrame with signals
        
        Returns:
            Dictionary with strategy statistics
        """
        buy_signals = (signals_df['signal'] == 1).sum()
        sell_signals = (signals_df['signal'] == -1).sum()
        
        # Calculate periods in position
        long_periods = (signals_df['position'] == 1).sum()
        flat_periods = (signals_df['position'] == 0).sum()
        short_periods = (signals_df['position'] == -1).sum()
        
        total_periods = len(signals_df)
        
        stats = {
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'long_periods': long_periods,
            'flat_periods': flat_periods,
            'short_periods': short_periods,
            'pct_time_in_market': ((long_periods + short_periods) / total_periods * 100) 
                                  if total_periods > 0 else 0
        }
        
        return stats


def main():
    """Example usage of SimpleMACrossStrategy."""
    import sys
    sys.path.append('..')
    
    from example_data_fetcher import DataFetcher
    import matplotlib.pyplot as plt
    
    print("=== Simple MA Crossover Strategy Example ===\n")
    
    # Fetch data
    fetcher = DataFetcher()
    data = fetcher.fetch_historical_data('SPY', '2022-01-01', '2024-01-01')
    
    if data is None:
        print("Failed to fetch data")
        return
    
    # Apply strategy
    strategy = SimpleMACrossStrategy(fast_period=50, slow_period=200)
    signals = strategy.generate_signals(data)
    
    # Get statistics
    stats = strategy.get_strategy_stats(signals)
    print("Strategy Statistics:")
    print(f"  Buy Signals: {stats['buy_signals']}")
    print(f"  Sell Signals: {stats['sell_signals']}")
    print(f"  Time in Market: {stats['pct_time_in_market']:.2f}%")
    print(f"  Long Periods: {stats['long_periods']}")
    print(f"  Flat Periods: {stats['flat_periods']}")
    
    # Plot the strategy
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # Plot prices and moving averages
    ax1.plot(signals.index, signals['close'], label='Close Price', alpha=0.7)
    ax1.plot(signals.index, signals['fast_ma'], label=f'Fast MA ({strategy.fast_period})', alpha=0.8)
    ax1.plot(signals.index, signals['slow_ma'], label=f'Slow MA ({strategy.slow_period})', alpha=0.8)
    
    # Plot buy/sell signals
    buy_signals = signals[signals['signal'] == 1]
    sell_signals = signals[signals['signal'] == -1]
    
    ax1.scatter(buy_signals.index, buy_signals['close'], 
               color='green', marker='^', s=100, label='Buy Signal', zorder=5)
    ax1.scatter(sell_signals.index, sell_signals['close'], 
               color='red', marker='v', s=100, label='Sell Signal', zorder=5)
    
    ax1.set_ylabel('Price ($)')
    ax1.set_title('SPY - Moving Average Crossover Strategy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot position
    ax2.fill_between(signals.index, 0, signals['position'], 
                     where=signals['position'] > 0, color='green', alpha=0.3, label='Long')
    ax2.fill_between(signals.index, 0, signals['position'], 
                     where=signals['position'] < 0, color='red', alpha=0.3, label='Short')
    ax2.set_ylabel('Position')
    ax2.set_xlabel('Date')
    ax2.set_title('Position Over Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/tmp/strategy_example.png', dpi=100)
    print("\nChart saved to /tmp/strategy_example.png")
    plt.show()


if __name__ == "__main__":
    main()
