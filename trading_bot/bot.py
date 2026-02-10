"""
Main trading bot module for live trading execution.
"""
import time
from datetime import datetime
from typing import Optional
from .data_fetcher import DataFetcher
from .indicators import Indicators
from .strategy import TradingStrategy
from .risk_manager import RiskManager
from .config import (
    SYMBOL, TIMEFRAME, INITIAL_BALANCE, EMA_SHORT, EMA_LONG, 
    RISK_PER_TRADE, LOOKBACK_DAYS
)


class TradingBot:
    """
    Main trading bot for live execution.
    """
    
    def __init__(self, initial_balance: float = INITIAL_BALANCE, 
                 use_testnet: bool = True):
        """
        Initialize trading bot.
        
        Args:
            initial_balance: Starting balance in USDT
            use_testnet: Whether to use testnet
        """
        self.data_fetcher = DataFetcher(testnet=use_testnet)
        self.strategy = TradingStrategy()
        self.risk_manager = RiskManager(initial_balance)
        self.running = False
        
        print(f"Trading Bot initialized with ${initial_balance:,.2f}")
        print(f"Using {'TESTNET' if use_testnet else 'LIVE'} mode")
    
    def fetch_and_prepare_data(self):
        """
        Fetch latest data and prepare with indicators.
        
        Returns:
            DataFrame with price data and indicators
        """
        # Fetch historical data
        df = self.data_fetcher.get_historical_data(
            symbol=SYMBOL,
            interval=TIMEFRAME,
            lookback_days=LOOKBACK_DAYS
        )
        
        # Add EMAs
        df = Indicators.add_emas(df, EMA_SHORT, EMA_LONG)
        
        return df
    
    def check_and_execute_trades(self, df, current_price: float, current_time: datetime):
        """
        Check for trade signals and execute if conditions are met.
        
        Args:
            df: DataFrame with price and indicator data
            current_price: Current market price
            current_time: Current timestamp
        """
        # Update existing positions
        closed_positions = self.strategy.update_positions(current_price, current_time)
        
        # Process closed positions
        for closed_pos in closed_positions:
            self.risk_manager.update_balance(closed_pos['pnl'], current_time)
            
            # Log trade closure
            print(f"\n{'='*60}")
            print(f"POSITION CLOSED: {closed_pos['exit_reason']}")
            print(f"Exit Price: ${closed_pos['exit_price']:,.2f}")
            print(f"P&L: ${closed_pos['pnl']:,.2f} ({closed_pos['pnl_percent']:.2f}%)")
            print(f"Entry Time: {closed_pos['entry_time']}")
            print(f"Exit Time: {closed_pos['exit_time']}")
            print(f"{'='*60}\n")
        
        # Check if can trade
        can_trade, reason = self.risk_manager.can_trade()
        
        if not can_trade:
            print(f"Trading halted: {reason}")
            return
        
        # Check entry signal
        if self.strategy.check_entry_signal(df):
            # Try to open position
            position = self.strategy.open_position(
                current_price,
                self.risk_manager.current_balance,
                RISK_PER_TRADE,
                df,
                current_time
            )
            
            if position:
                print(f"\n{'='*60}")
                print("NEW POSITION OPENED")
                print(f"Entry Price: ${position.entry_price:,.2f}")
                print(f"Quantity: {position.quantity:.6f} BTC")
                print(f"Stop Loss: ${position.stop_loss:,.2f}")
                print(f"Take Profit: ${position.take_profit:,.2f}")
                print(f"Entry Time: {position.entry_time}")
                print(f"{'='*60}\n")
            else:
                print("Entry signal detected but couldn't open position (max positions reached)")
    
    def print_status(self, current_price: float):
        """
        Print current bot status.
        
        Args:
            current_price: Current market price
        """
        print(f"\n{'-'*60}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current Price: ${current_price:,.2f}")
        
        # Risk manager stats
        stats = self.risk_manager.get_stats()
        print(f"Balance: ${stats['current_balance']:,.2f}")
        print(f"Total P&L: ${stats['total_pnl']:,.2f} ({stats['total_return_percent']:.2f}%)")
        print(f"Daily P&L: ${stats['daily_pnl']:,.2f} ({stats['daily_return_percent']:.2f}%)")
        
        # Open positions
        open_positions = self.strategy.get_open_positions_summary(current_price)
        print(f"Open Positions: {len(open_positions)}/{MAX_POSITIONS}")
        
        if open_positions:
            print("\nPosition Details:")
            for pos in open_positions:
                print(f"  - Entry: ${pos['entry_price']:,.2f} | "
                      f"Current: ${pos['current_price']:,.2f} | "
                      f"P&L: ${pos['pnl']:,.2f} ({pos['pnl_percent']:.2f}%) | "
                      f"Trailing: {pos['trailing_active']}")
        
        print(f"{'-'*60}\n")
    
    def run_once(self):
        """
        Run one iteration of the trading bot.
        """
        try:
            # Fetch and prepare data
            df = self.fetch_and_prepare_data()
            
            # Get current price
            current_price = self.data_fetcher.get_current_price(SYMBOL)
            current_time = datetime.now()
            
            # Print status
            self.print_status(current_price)
            
            # Check and execute trades
            self.check_and_execute_trades(df, current_price, current_time)
            
        except Exception as e:
            print(f"Error in trading iteration: {e}")
    
    def run_live(self, check_interval: int = 300):
        """
        Run bot in live mode with periodic checks.
        
        Args:
            check_interval: Seconds between checks (default: 300 = 5 minutes)
        """
        self.running = True
        print(f"\nStarting live trading bot...")
        print(f"Check interval: {check_interval} seconds")
        print(f"Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                self.run_once()
                
                # Wait for next check
                print(f"Waiting {check_interval} seconds until next check...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\nStopping trading bot...")
            self.stop()
    
    def stop(self):
        """
        Stop the trading bot.
        """
        self.running = False
        
        # Print final summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        stats = self.risk_manager.get_stats()
        print(f"Initial Balance: ${stats['initial_balance']:,.2f}")
        print(f"Final Balance: ${stats['current_balance']:,.2f}")
        print(f"Total Return: {stats['total_return_percent']:.2f}%")
        print(f"Total Trades: {len(self.strategy.closed_positions)}")
        print("="*60 + "\n")
