"""
Example: Simple Backtester
This module demonstrates how to backtest a trading strategy.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt


class SimpleBacktester:
    """
    Simple backtesting engine for trading strategies.
    
    This backtester:
    - Simulates trading based on signals
    - Tracks portfolio value over time
    - Calculates performance metrics
    - Handles transaction costs
    
    Example usage:
        backtester = SimpleBacktester(initial_capital=10000, commission=0.001)
        results = backtester.run(signals_df)
        backtester.print_results()
    """
    
    def __init__(self, initial_capital: float = 10000, commission: float = 0.001):
        """
        Initialize the backtester.
        
        Args:
            initial_capital: Starting capital in dollars
            commission: Commission per trade as a fraction (0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.trades = []
        self.portfolio_values = []
    
    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Run backtest on data with signals.
        
        Args:
            data: DataFrame with 'close', 'signal', and 'position' columns
        
        Returns:
            DataFrame with portfolio values and returns
        """
        df = data.copy()
        
        # Initialize portfolio tracking
        cash = self.initial_capital
        position = 0  # Number of shares held
        portfolio_value = self.initial_capital
        
        portfolio_values = []
        
        for idx, row in df.iterrows():
            price = row['close']
            signal = row['signal']
            
            # Execute trade based on signal
            if signal == 1 and position == 0:  # Buy signal
                # Buy as many shares as possible
                shares_to_buy = int(cash / (price * (1 + self.commission)))
                if shares_to_buy > 0:
                    cost = shares_to_buy * price * (1 + self.commission)
                    cash -= cost
                    position += shares_to_buy
                    
                    self.trades.append({
                        'date': idx,
                        'type': 'BUY',
                        'shares': shares_to_buy,
                        'price': price,
                        'cost': cost
                    })
            
            elif signal == -1 and position > 0:  # Sell signal
                # Sell all shares
                proceeds = position * price * (1 - self.commission)
                cash += proceeds
                
                self.trades.append({
                    'date': idx,
                    'type': 'SELL',
                    'shares': position,
                    'price': price,
                    'proceeds': proceeds
                })
                
                position = 0
            
            # Calculate current portfolio value
            portfolio_value = cash + (position * price)
            portfolio_values.append({
                'date': idx,
                'portfolio_value': portfolio_value,
                'cash': cash,
                'position': position,
                'price': price
            })
        
        # Create results DataFrame
        results_df = pd.DataFrame(portfolio_values)
        results_df.set_index('date', inplace=True)
        
        # Calculate returns
        results_df['returns'] = results_df['portfolio_value'].pct_change()
        results_df['cumulative_returns'] = (1 + results_df['returns']).cumprod() - 1
        
        self.results = results_df
        return results_df
    
    def calculate_metrics(self) -> Dict:
        """
        Calculate performance metrics.
        
        Returns:
            Dictionary with performance metrics
        """
        if not hasattr(self, 'results'):
            return {}
        
        total_return = ((self.results['portfolio_value'].iloc[-1] / self.initial_capital) - 1) * 100
        
        # Calculate maximum drawdown
        cumulative_max = self.results['portfolio_value'].cummax()
        drawdown = (self.results['portfolio_value'] - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min() * 100
        
        # Calculate Sharpe ratio (assuming 252 trading days per year)
        returns = self.results['returns'].dropna()
        if len(returns) > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0
        else:
            sharpe_ratio = 0
        
        # Trade statistics
        num_trades = len(self.trades)
        buy_trades = [t for t in self.trades if t['type'] == 'BUY']
        sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        
        # Calculate win rate
        winning_trades = 0
        total_closed_trades = 0
        
        for i, buy in enumerate(buy_trades):
            if i < len(sell_trades):
                sell = sell_trades[i]
                profit = sell['proceeds'] - buy['cost']
                if profit > 0:
                    winning_trades += 1
                total_closed_trades += 1
        
        win_rate = (winning_trades / total_closed_trades * 100) if total_closed_trades > 0 else 0
        
        metrics = {
            'initial_capital': self.initial_capital,
            'final_value': self.results['portfolio_value'].iloc[-1],
            'total_return_pct': total_return,
            'max_drawdown_pct': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'num_trades': num_trades,
            'win_rate_pct': win_rate,
            'num_winning_trades': winning_trades,
            'num_losing_trades': total_closed_trades - winning_trades
        }
        
        return metrics
    
    def print_results(self):
        """Print backtest results in a formatted way."""
        metrics = self.calculate_metrics()
        
        print("\n" + "="*50)
        print("BACKTEST RESULTS")
        print("="*50)
        print(f"Initial Capital:        ${metrics['initial_capital']:,.2f}")
        print(f"Final Portfolio Value:  ${metrics['final_value']:,.2f}")
        print(f"Total Return:           {metrics['total_return_pct']:,.2f}%")
        print(f"Max Drawdown:           {metrics['max_drawdown_pct']:,.2f}%")
        print(f"Sharpe Ratio:           {metrics['sharpe_ratio']:.2f}")
        print(f"\nNumber of Trades:       {metrics['num_trades']}")
        print(f"Winning Trades:         {metrics['num_winning_trades']}")
        print(f"Losing Trades:          {metrics['num_losing_trades']}")
        print(f"Win Rate:               {metrics['win_rate_pct']:.2f}%")
        print("="*50 + "\n")
    
    def plot_results(self, save_path: str = None):
        """
        Plot backtest results.
        
        Args:
            save_path: Optional path to save the plot
        """
        if not hasattr(self, 'results'):
            print("No results to plot. Run backtest first.")
            return
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Plot 1: Portfolio Value
        axes[0].plot(self.results.index, self.results['portfolio_value'], 
                    label='Portfolio Value', linewidth=2)
        axes[0].axhline(y=self.initial_capital, color='r', linestyle='--', 
                       label='Initial Capital', alpha=0.7)
        axes[0].set_ylabel('Portfolio Value ($)')
        axes[0].set_title('Portfolio Value Over Time')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Cumulative Returns
        axes[1].plot(self.results.index, self.results['cumulative_returns'] * 100, 
                    label='Cumulative Returns', linewidth=2, color='green')
        axes[1].axhline(y=0, color='r', linestyle='--', alpha=0.7)
        axes[1].set_ylabel('Cumulative Returns (%)')
        axes[1].set_title('Cumulative Returns Over Time')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Drawdown
        cumulative_max = self.results['portfolio_value'].cummax()
        drawdown = (self.results['portfolio_value'] - cumulative_max) / cumulative_max * 100
        axes[2].fill_between(self.results.index, 0, drawdown, 
                            color='red', alpha=0.3, label='Drawdown')
        axes[2].set_ylabel('Drawdown (%)')
        axes[2].set_xlabel('Date')
        axes[2].set_title('Drawdown Over Time')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=100)
            print(f"Plot saved to {save_path}")
        
        plt.show()


def main():
    """Example usage of SimpleBacktester."""
    import sys
    sys.path.append('..')
    
    from example_data_fetcher import DataFetcher
    from example_strategy import SimpleMACrossStrategy
    
    print("=== Simple Backtester Example ===\n")
    
    # Step 1: Fetch data
    print("1. Fetching data...")
    fetcher = DataFetcher()
    data = fetcher.fetch_historical_data('SPY', '2020-01-01', '2024-01-01')
    
    if data is None:
        print("Failed to fetch data")
        return
    
    print(f"   Fetched {len(data)} days of data")
    
    # Step 2: Generate signals
    print("\n2. Generating trading signals...")
    strategy = SimpleMACrossStrategy(fast_period=50, slow_period=200)
    signals = strategy.generate_signals(data)
    
    stats = strategy.get_strategy_stats(signals)
    print(f"   Generated {stats['buy_signals']} buy signals and {stats['sell_signals']} sell signals")
    
    # Step 3: Run backtest
    print("\n3. Running backtest...")
    backtester = SimpleBacktester(initial_capital=10000, commission=0.001)
    results = backtester.run(signals)
    
    # Step 4: Print and plot results
    backtester.print_results()
    backtester.plot_results(save_path='/tmp/backtest_results.png')


if __name__ == "__main__":
    main()
