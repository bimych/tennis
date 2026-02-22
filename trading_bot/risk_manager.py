"""
Risk management module for enforcing trading limits and safeguards.
"""
from typing import List, Dict
from datetime import datetime, date
from .config import MAX_DAILY_LOSS, RISK_PER_TRADE


class RiskManager:
    """
    Manages risk limits and trading safeguards.
    """
    
    def __init__(self, initial_balance: float):
        """
        Initialize risk manager.
        
        Args:
            initial_balance: Starting balance in USDT
        """
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.daily_start_balance = initial_balance
        self.daily_pnl = 0.0
        self.current_date = date.today()
        self.trading_halted = False
        self.halt_reason = ""
    
    def reset_daily_tracking(self):
        """
        Reset daily tracking at the start of a new day.
        """
        self.current_date = date.today()
        self.daily_start_balance = self.current_balance
        self.daily_pnl = 0.0
        self.trading_halted = False
        self.halt_reason = ""
    
    def update_balance(self, pnl: float, current_time: datetime):
        """
        Update current balance and daily P&L.
        
        Args:
            pnl: Profit/loss from closed position
            current_time: Current timestamp
        """
        # Check if new day
        if current_time.date() != self.current_date:
            self.reset_daily_tracking()
        
        # Update balances
        self.current_balance += pnl
        self.daily_pnl += pnl
        
        # Check daily loss limit
        self.check_daily_loss_limit()
    
    def check_daily_loss_limit(self) -> bool:
        """
        Check if daily loss limit has been reached.
        
        Returns:
            True if limit reached, False otherwise
        """
        daily_loss_percent = self.daily_pnl / self.daily_start_balance
        
        if daily_loss_percent <= -MAX_DAILY_LOSS:
            self.trading_halted = True
            self.halt_reason = f"Daily loss limit reached: {daily_loss_percent*100:.2f}%"
            return True
        
        return False
    
    def can_trade(self) -> tuple[bool, str]:
        """
        Check if trading is allowed.
        
        Returns:
            Tuple of (can_trade, reason)
        """
        if self.trading_halted:
            return False, self.halt_reason
        
        if self.current_balance <= 0:
            return False, "Account balance depleted"
        
        return True, ""
    
    def get_risk_amount(self) -> float:
        """
        Get the risk amount for the next trade.
        
        Returns:
            Risk amount in USDT
        """
        return self.current_balance * RISK_PER_TRADE
    
    def get_stats(self) -> Dict:
        """
        Get risk management statistics.
        
        Returns:
            Dictionary with risk statistics
        """
        total_pnl = self.current_balance - self.initial_balance
        total_return = (total_pnl / self.initial_balance) * 100
        
        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'total_pnl': total_pnl,
            'total_return_percent': total_return,
            'daily_pnl': self.daily_pnl,
            'daily_return_percent': (self.daily_pnl / self.daily_start_balance) * 100,
            'trading_halted': self.trading_halted,
            'halt_reason': self.halt_reason
        }
