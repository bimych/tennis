"""
Backtesting framework for testing trading strategy on historical data.
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
from .indicators import Indicators
from .strategy import TradingStrategy
from .risk_manager import RiskManager
from .config import (
    INITIAL_BALANCE, EMA_SHORT, EMA_LONG, RISK_PER_TRADE
)


class Backtester:
    """
    Backtest trading strategy on historical data.
    """
    
    def __init__(self, data: pd.DataFrame, initial_balance: float = INITIAL_BALANCE):
        """
        Initialize backtester.
        
        Args:
            data: Historical OHLCV data
            initial_balance: Starting balance in USDT
        """
        self.data = data.copy()
        self.initial_balance = initial_balance
        self.strategy = TradingStrategy()
        self.risk_manager = RiskManager(initial_balance)
        self.trades_log: List[Dict] = []
        self.equity_curve: List[float] = []
    
    def run(self) -> Dict:
        """
        Run backtest on historical data.
        
        Returns:
            Dictionary with backtest results
        """
        # Add EMAs to data
        self.data = Indicators.add_emas(self.data, EMA_SHORT, EMA_LONG)
        
        # Iterate through each candle
        for i in range(len(self.data)):
            current_candle = self.data.iloc[i]
            current_price = current_candle['close']
            current_time = current_candle['timestamp']
            
            # Get historical data up to current point
            historical_df = self.data.iloc[:i+1]
            
            # Update existing positions
            closed_positions = self.strategy.update_positions(current_price, current_time)
            
            # Update risk manager with closed positions
            for closed_pos in closed_positions:
                self.risk_manager.update_balance(closed_pos['pnl'], current_time)
                self.trades_log.append(closed_pos)
                
                # Log trade
                print(f"CLOSED: {closed_pos['exit_reason']} at {current_price:.2f} | "
                      f"P&L: ${closed_pos['pnl']:.2f} ({closed_pos['pnl_percent']:.2f}%)")
            
            # Check if can trade
            can_trade, reason = self.risk_manager.can_trade()
            
            if can_trade and i >= EMA_LONG:
                # Check entry signal
                if self.strategy.check_entry_signal(historical_df):
                    # Try to open position
                    position = self.strategy.open_position(
                        current_price,
                        self.risk_manager.current_balance,
                        RISK_PER_TRADE,
                        historical_df,
                        current_time
                    )
                    
                    if position:
                        print(f"OPENED: Buy at {current_price:.2f} | "
                              f"SL: {position.stop_loss:.2f} | TP: {position.take_profit:.2f} | "
                              f"Qty: {position.quantity:.6f}")
            
            # Track equity
            self.equity_curve.append(self.risk_manager.current_balance)
        
        # Close any remaining positions at final price
        final_price = self.data.iloc[-1]['close']
        final_time = self.data.iloc[-1]['timestamp']
        for position in self.strategy.positions:
            pnl = position.get_pnl(final_price)
            closed_pos = {
                'entry_price': position.entry_price,
                'exit_price': final_price,
                'quantity': position.quantity,
                'pnl': pnl,
                'pnl_percent': (pnl / (position.entry_price * position.quantity)) * 100,
                'entry_time': position.entry_time,
                'exit_time': final_time,
                'exit_reason': 'Backtest End'
            }
            self.risk_manager.update_balance(pnl, final_time)
            self.trades_log.append(closed_pos)
        
        self.strategy.positions = []
        
        # Calculate performance metrics
        return self.calculate_performance_metrics()
    
    def calculate_performance_metrics(self) -> Dict:
        """
        Calculate performance metrics from backtest results.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades_log:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'final_balance': self.initial_balance,
                'total_return': 0,
                'avg_win': 0,
                'avg_loss': 0
            }
        
        # Separate winning and losing trades
        winning_trades = [t for t in self.trades_log if t['pnl'] > 0]
        losing_trades = [t for t in self.trades_log if t['pnl'] <= 0]
        
        # Basic metrics
        total_trades = len(self.trades_log)
        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
        
        # Profit factor
        total_wins = sum(t['pnl'] for t in winning_trades) if winning_trades else 0
        total_losses = abs(sum(t['pnl'] for t in losing_trades)) if losing_trades else 0
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        # Average win/loss
        avg_win = total_wins / len(winning_trades) if winning_trades else 0
        avg_loss = total_losses / len(losing_trades) if losing_trades else 0
        
        # Drawdown
        max_drawdown = self.calculate_max_drawdown()
        
        # Final metrics
        final_balance = self.risk_manager.current_balance
        total_return = ((final_balance - self.initial_balance) / self.initial_balance) * 100
        
        return {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'initial_balance': self.initial_balance,
            'final_balance': final_balance,
            'total_return': total_return,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'total_pnl': final_balance - self.initial_balance
        }
    
    def calculate_max_drawdown(self) -> float:
        """
        Calculate maximum drawdown from equity curve.
        
        Returns:
            Maximum drawdown percentage
        """
        if not self.equity_curve:
            return 0
        
        equity_array = np.array(self.equity_curve)
        running_max = np.maximum.accumulate(equity_array)
        drawdown = (equity_array - running_max) / running_max * 100
        max_drawdown = abs(drawdown.min())
        
        return max_drawdown
    
    def get_trades_summary(self) -> pd.DataFrame:
        """
        Get summary of all trades as DataFrame.
        
        Returns:
            DataFrame with trade details
        """
        if not self.trades_log:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades_log)
    
    def print_results(self):
        """
        Print backtest results to console.
        """
        metrics = self.calculate_performance_metrics()
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(f"Initial Balance: ${metrics['initial_balance']:,.2f}")
        print(f"Final Balance: ${metrics['final_balance']:,.2f}")
        print(f"Total Return: {metrics['total_return']:.2f}%")
        print(f"Total P&L: ${metrics['total_pnl']:,.2f}")
        print("-"*60)
        print(f"Total Trades: {metrics['total_trades']}")
        print(f"Winning Trades: {metrics['winning_trades']}")
        print(f"Losing Trades: {metrics['losing_trades']}")
        print(f"Win Rate: {metrics['win_rate']:.2f}%")
        print(f"Profit Factor: {metrics['profit_factor']:.2f}")
        print(f"Average Win: ${metrics['avg_win']:.2f}")
        print(f"Average Loss: ${metrics['avg_loss']:.2f}")
        print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
        print("="*60 + "\n")
