#!/usr/bin/env python3
"""
Run live trading bot with Binance API.
"""
import sys
import argparse
from trading_bot.bot import TradingBot
from trading_bot.config import INITIAL_BALANCE, USE_TESTNET


def main():
    """
    Main function to run live trading bot.
    """
    parser = argparse.ArgumentParser(description='BTC/USDT Trading Bot')
    parser.add_argument('--balance', type=float, default=INITIAL_BALANCE,
                       help=f'Initial balance in USDT (default: {INITIAL_BALANCE})')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300)')
    parser.add_argument('--testnet', action='store_true', default=USE_TESTNET,
                       help='Use Binance testnet (default: based on config)')
    parser.add_argument('--live', action='store_true',
                       help='Use live Binance API (overrides testnet)')
    
    args = parser.parse_args()
    
    # Determine testnet mode
    use_testnet = not args.live if args.live else args.testnet
    
    print("="*60)
    print("BTC/USDT TRADING BOT - LIVE MODE")
    print("="*60)
    print(f"Mode: {'TESTNET' if use_testnet else 'LIVE TRADING'}")
    print(f"Initial Balance: ${args.balance:,.2f}")
    print(f"Check Interval: {args.interval} seconds")
    print("="*60 + "\n")
    
    if not use_testnet:
        confirm = input("WARNING: You are about to run in LIVE mode with real funds. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
    
    try:
        # Initialize and run bot
        bot = TradingBot(initial_balance=args.balance, use_testnet=use_testnet)
        bot.run_live(check_interval=args.interval)
        
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"\nError running bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
