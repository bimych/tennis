# Tennis Schedule Checker & Trading Bot

This repository contains two independent projects:

## 1. Tennis Schedule Checker

A web scraper that checks for available beginner tennis classes at Tower Hamlets tennis facilities.

**Main file:** `check_tennis_schedule.py`

### Features
- Scrapes tennis class schedules from tennistowerhamlets.com
- Filters for beginner classes
- Checks availability (minimum spaces requirement)
- Sends email notifications via SendGrid

### Usage
```bash
python check_tennis_schedule.py
```

Requires:
- `SENDGRID_API_KEY` environment variable in `.env` file

---

## 2. BTC/USDT Trading Bot

A trend-following cryptocurrency trading bot for the BTC/USDT market on Binance.

**Documentation:** See [TRADING_BOT_README.md](TRADING_BOT_README.md) for complete details.

### Quick Start

**Test with Demo Data (No Internet Required):**
```bash
python run_demo_backtest.py
```

**Run Tests:**
```bash
python test_trading_bot.py
```

**Backtest with Real Data:**
```bash
python run_backtest.py
```

**Live Trading (Testnet):**
```bash
python run_live.py --testnet
```

### Features
- EMA-based trend-following strategy
- Automated position sizing (1% risk per trade)
- Trailing stop loss
- Daily loss limits (3% halt)
- Backtesting framework with performance metrics
- Console-based logging

### Main Components
- `trading_bot/` - Core bot modules
- `run_demo_backtest.py` - Demo backtesting with simulated data
- `run_backtest.py` - Backtest with real Binance data
- `run_live.py` - Live trading mode
- `test_trading_bot.py` - Test suite

---

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# For tennis checker
SENDGRID_API_KEY=your_sendgrid_key

# For trading bot (optional, only for live/testnet trading)
BINANCE_API_KEY=your_binance_key
BINANCE_API_SECRET=your_binance_secret
USE_TESTNET=True
```

## License

MIT License
