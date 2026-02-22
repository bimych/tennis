#!/usr/bin/env python3
"""
Run backtesting on demo/simulated BTC/USDT data (no internet required).
This is useful for testing the bot logic without needing Binance API access.
"""
import sys
from trading_bot.demo_data import DemoDataGenerator
from trading_bot.backtester import Backtester
from trading_bot.config import INITIAL_BALANCE


def main():
    """
    Main function to run demo backtest.
    """
    print("="*60)
    print("BTC/USDT TRADING BOT - DEMO BACKTESTING")
    print("="*60)
    print("Using simulated price data (no internet required)")
    print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
    print("="*60 + "\n")
    
    try:
        # Generate demo data
        print("Generating demo price data...")
        df = DemoDataGenerator.generate_demo_data(
            start_price=50000.0,
            num_candles=2160,  # 90 days of 1-hour candles
            volatility=0.02
        )
        
        print(f"Generated {len(df)} candles from {df['timestamp'].min()} to {df['timestamp'].max()}\n")
        
        # Run backtest
        print("Running backtest on demo data...\n")
        backtester = Backtester(df, INITIAL_BALANCE)
        results = backtester.run()
        
        # Print results
        backtester.print_results()
        
        # Print trade details
        trades_df = backtester.get_trades_summary()
        if not trades_df.empty:
            print("\nFirst 5 Trades:")
            print(trades_df.head().to_string())
            if len(trades_df) > 5:
                print(f"\n... and {len(trades_df) - 5} more trades")
        else:
            print("\nNo trades were executed during the backtest period.")
        
        print("\nNOTE: This was a demo backtest using simulated data.")
        print("For real backtesting, use run_backtest.py with internet access.")
        
    except Exception as e:
        print(f"\nError running demo backtest: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
