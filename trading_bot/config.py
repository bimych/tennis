"""
Configuration module for the BTC/USDT trading bot.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Binance API Configuration
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
USE_TESTNET = os.getenv('USE_TESTNET', 'True').lower() == 'true'

# Trading Configuration
SYMBOL = 'BTCUSDT'
TIMEFRAME = '1h'
EMA_SHORT = 20
EMA_LONG = 50

# Entry/Exit Configuration
ENTRY_PRICE_TOLERANCE = 0.01  # 1% from EMA 20
RISK_REWARD_RATIO = 2.0  # 2:1 reward to risk
TRAILING_STOP_PERCENT = 0.01  # 1% trailing stop

# Risk Management
RISK_PER_TRADE = 0.01  # 1% of portfolio per trade
MAX_POSITIONS = 3
MAX_DAILY_LOSS = 0.03  # 3% daily loss limit

# Backtesting Configuration
INITIAL_BALANCE = 10000  # Starting balance in USDT for backtesting
LOOKBACK_DAYS = 90  # Days of historical data for backtesting
