"""
Trading strategy implementation for trend-following with EMA.
"""
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime
from .indicators import Indicators
from .config import (
    EMA_SHORT, EMA_LONG, ENTRY_PRICE_TOLERANCE, 
    RISK_REWARD_RATIO, TRAILING_STOP_PERCENT, MAX_POSITIONS
)


class Position:
    """
    Represents an open trading position.
    """
    
    def __init__(self, entry_price: float, quantity: float, stop_loss: float, 
                 take_profit: float, entry_time: datetime):
        """
        Initialize a position.
        
        Args:
            entry_price: Entry price
            quantity: Position size
            stop_loss: Initial stop loss price
            take_profit: Take profit price
            entry_time: Entry timestamp
        """
        self.entry_price = entry_price
        self.quantity = quantity
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_time = entry_time
        self.trailing_stop_active = False
        self.highest_price = entry_price
    
    def update_trailing_stop(self, current_price: float, trailing_percent: float = TRAILING_STOP_PERCENT):
        """
        Update trailing stop if price is in profit.
        
        Args:
            current_price: Current market price
            trailing_percent: Trailing stop percentage
        """
        # Check if position is in profit
        if current_price > self.entry_price:
            self.trailing_stop_active = True
            self.highest_price = max(self.highest_price, current_price)
            # Update stop loss to trailing stop
            new_stop = self.highest_price * (1 - trailing_percent)
            self.stop_loss = max(self.stop_loss, new_stop)
    
    def should_exit(self, current_price: float) -> tuple[bool, str]:
        """
        Check if position should be exited.
        
        Args:
            current_price: Current market price
            
        Returns:
            Tuple of (should_exit, reason)
        """
        if current_price <= self.stop_loss:
            return True, "Stop Loss"
        if current_price >= self.take_profit:
            return True, "Take Profit"
        return False, ""
    
    def get_pnl(self, current_price: float) -> float:
        """
        Calculate current profit/loss.
        
        Args:
            current_price: Current market price
            
        Returns:
            Profit/loss in USDT
        """
        return (current_price - self.entry_price) * self.quantity


class TradingStrategy:
    """
    Implements the trend-following trading strategy.
    """
    
    def __init__(self):
        """
        Initialize trading strategy.
        """
        self.positions: List[Position] = []
        self.closed_positions: List[Dict] = []
    
    def can_open_position(self) -> bool:
        """
        Check if we can open a new position based on position limits.
        
        Returns:
            True if can open position, False otherwise
        """
        return len(self.positions) < MAX_POSITIONS
    
    def check_entry_signal(self, df: pd.DataFrame) -> bool:
        """
        Check if entry conditions are met.
        
        Args:
            df: DataFrame with price data and EMAs
            
        Returns:
            True if entry signal detected, False otherwise
        """
        if len(df) < EMA_LONG:
            return False
        
        # Get latest values
        latest = df.iloc[-1]
        current_price = latest['close']
        ema_short = latest['ema_short']
        ema_long = latest['ema_long']
        
        # Check conditions:
        # 1. EMA 20 > EMA 50 (uptrend)
        # 2. Price within 1% of EMA 20
        is_uptrend = Indicators.is_uptrend(ema_short, ema_long)
        is_near_ema = Indicators.is_price_near_ema(current_price, ema_short, ENTRY_PRICE_TOLERANCE)
        
        return is_uptrend and is_near_ema
    
    def calculate_position_size(self, entry_price: float, stop_loss: float, 
                                account_balance: float, risk_percent: float) -> float:
        """
        Calculate position size based on risk management.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            account_balance: Account balance in USDT
            risk_percent: Risk percentage per trade
            
        Returns:
            Position size in base currency
        """
        risk_amount = account_balance * risk_percent
        price_diff = abs(entry_price - stop_loss)
        
        if price_diff == 0:
            return 0
        
        position_size = risk_amount / price_diff
        return position_size
    
    def open_position(self, entry_price: float, account_balance: float, 
                     risk_percent: float, df: pd.DataFrame, 
                     entry_time: datetime) -> Optional[Position]:
        """
        Open a new trading position.
        
        Args:
            entry_price: Entry price
            account_balance: Current account balance
            risk_percent: Risk percentage per trade
            df: DataFrame with price data
            entry_time: Entry timestamp
            
        Returns:
            Position object if opened, None otherwise
        """
        if not self.can_open_position():
            return None
        
        # Calculate stop loss (swing low)
        stop_loss = Indicators.find_swing_low(df, lookback=10)
        
        # Ensure stop loss is below entry
        if stop_loss >= entry_price:
            stop_loss = entry_price * 0.98  # Default 2% stop loss
        
        # Calculate take profit (2R)
        risk = entry_price - stop_loss
        take_profit = entry_price + (risk * RISK_REWARD_RATIO)
        
        # Calculate position size
        quantity = self.calculate_position_size(entry_price, stop_loss, account_balance, risk_percent)
        
        if quantity <= 0:
            return None
        
        # Create position
        position = Position(entry_price, quantity, stop_loss, take_profit, entry_time)
        self.positions.append(position)
        
        return position
    
    def update_positions(self, current_price: float, current_time: datetime) -> List[Dict]:
        """
        Update all open positions and check for exits.
        
        Args:
            current_price: Current market price
            current_time: Current timestamp
            
        Returns:
            List of closed position dictionaries
        """
        closed = []
        remaining_positions = []
        
        for position in self.positions:
            # Update trailing stop
            position.update_trailing_stop(current_price)
            
            # Check if should exit
            should_exit, reason = position.should_exit(current_price)
            
            if should_exit:
                # Close position
                pnl = position.get_pnl(current_price)
                closed_position = {
                    'entry_price': position.entry_price,
                    'exit_price': current_price,
                    'quantity': position.quantity,
                    'pnl': pnl,
                    'pnl_percent': (pnl / (position.entry_price * position.quantity)) * 100,
                    'entry_time': position.entry_time,
                    'exit_time': current_time,
                    'exit_reason': reason
                }
                closed.append(closed_position)
                self.closed_positions.append(closed_position)
            else:
                remaining_positions.append(position)
        
        self.positions = remaining_positions
        return closed
    
    def get_open_positions_summary(self, current_price: float) -> List[Dict]:
        """
        Get summary of all open positions.
        
        Args:
            current_price: Current market price
            
        Returns:
            List of position summaries
        """
        summaries = []
        for i, position in enumerate(self.positions):
            pnl = position.get_pnl(current_price)
            summaries.append({
                'position_id': i,
                'entry_price': position.entry_price,
                'current_price': current_price,
                'quantity': position.quantity,
                'stop_loss': position.stop_loss,
                'take_profit': position.take_profit,
                'pnl': pnl,
                'pnl_percent': (pnl / (position.entry_price * position.quantity)) * 100,
                'trailing_active': position.trailing_stop_active
            })
        return summaries
