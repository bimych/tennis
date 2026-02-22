#!/usr/bin/env python3
"""
Run backtesting on historical BTC/USDT data.
"""
import sys
from trading_bot.data_fetcher import DataFetcher
from trading_bot.backtester import Backtester
from trading_bot.config import SYMBOL, TIMEFRAME, LOOKBACK_DAYS, INITIAL_BALANCE


def main():
    """
    Main function to run backtest.
    """
    print("="*60)
    print("BTC/USDT TRADING BOT - BACKTESTING")
    print("="*60)
    print(f"Symbol: {SYMBOL}")
    print(f"Timeframe: {TIMEFRAME}")
    print(f"Lookback Period: {LOOKBACK_DAYS} days")
    print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
    print("="*60 + "\n")
    
    try:
        # Initialize data fetcher (use public API, no auth needed for historical data)
        print("Fetching historical data from Binance...")
        data_fetcher = DataFetcher(api_key='', api_secret='', testnet=False)
        
        # Fetch historical data
        df = data_fetcher.get_historical_data(
            symbol=SYMBOL,
            interval=TIMEFRAME,
            lookback_days=LOOKBACK_DAYS
        )
        
        print(f"Loaded {len(df)} candles from {df['timestamp'].min()} to {df['timestamp'].max()}\n")
        
        # Run backtest
        print("Running backtest...\n")
        backtester = Backtester(df, INITIAL_BALANCE)
        results = backtester.run()
        
        # Print results
        backtester.print_results()
        
        # Print trade details
        trades_df = backtester.get_trades_summary()
        if not trades_df.empty:
            print("\nFirst 5 Trades:")
            print(trades_df.head().to_string())
            print(f"\n... and {max(0, len(trades_df) - 5)} more trades")
        
    except Exception as e:
        print(f"\nError running backtest: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
