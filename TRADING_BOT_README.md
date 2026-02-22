# BTC/USDT Trading Bot

A trend-following trading bot for the BTC/USDT market on Binance using EMA (Exponential Moving Average) indicators.

## Features

- **Trend-Following Strategy**: Uses EMA 20 and EMA 50 crossover strategy
- **Risk Management**: 
  - 1% risk per trade
  - Maximum 3 open positions
  - 3% daily loss limit with automatic trading halt
- **Dynamic Stop Loss**: Trailing stop that adjusts to 1% below current price when in profit
- **Take Profit**: 2:1 reward-to-risk ratio
- **Backtesting**: Test strategy on historical data before live trading
- **Console Logging**: Real-time trade notifications and daily summaries

## Strategy Details

### Entry Conditions
1. EMA 20 > EMA 50 (uptrend confirmed)
2. Current price within 1% of EMA 20
3. Maximum of 3 positions not reached

### Exit Conditions
- **Stop Loss**: Recent swing low (minimum 10 candles lookback)
- **Take Profit**: 2R (2x the risk amount)
- **Trailing Stop**: Activates when position is in profit, maintains 1% below highest price

### Risk Management
- Position sizing based on 1% account risk per trade
- Automatic trading halt after 3% daily loss
- Maximum 3 concurrent positions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bimych/tennis.git
cd tennis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Binance API credentials:
```bash
# For Testnet (recommended for testing)
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
USE_TESTNET=True

# For Live Trading (use with caution)
# BINANCE_API_KEY=your_live_api_key
# BINANCE_API_SECRET=your_live_api_secret
# USE_TESTNET=False
```

## Usage

### Demo Backtesting (Offline)

Run backtesting with simulated data (no internet or API credentials required):

```bash
python run_demo_backtest.py
```

This is perfect for:
- Testing the bot logic without internet access
- Quick verification that everything is working
- Understanding how the strategy behaves

### Backtesting (Online)

Run backtesting on real historical data from Binance (requires internet, no API credentials needed):

```bash
python run_backtest.py
```

This will:
- Fetch 90 days of historical BTC/USDT 1-hour candles from Binance
- Simulate trading with the strategy
- Display performance metrics including:
  - Win rate
  - Profit factor
  - Maximum drawdown
  - Total return
  - Average win/loss

### Live Trading (Testnet)

Run the bot with Binance Testnet (safe for testing):

```bash
python run_live.py --testnet
```

Optional parameters:
- `--balance`: Initial balance in USDT (default: 10000)
- `--interval`: Check interval in seconds (default: 300)

### Live Trading (Real Money)

**WARNING: Use with caution! This involves real money.**

```bash
python run_live.py --live --balance 1000
```

The bot will ask for confirmation before starting live trading.

### Testing

Run the test suite to verify all components are working correctly:

```bash
python test_trading_bot.py
```

This will test:
- EMA indicator calculations
- Uptrend detection logic
- Price proximity checks
- Position management (entry, exit, trailing stop)
- Risk management functionality
- Demo data generation

## Configuration

Edit `trading_bot/config.py` to customize:

```python
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
INITIAL_BALANCE = 10000
LOOKBACK_DAYS = 90
```

## Project Structure

```
trading_bot/
├── __init__.py           # Package initialization
├── config.py            # Configuration settings
├── data_fetcher.py      # Binance API data fetching
├── indicators.py        # Technical indicators (EMA)
├── strategy.py          # Trading strategy logic
├── risk_manager.py      # Risk management
├── backtester.py        # Backtesting framework
└── bot.py              # Main trading bot

run_backtest.py          # Backtesting script
run_live.py              # Live trading script
```

## Getting Binance API Keys

### Testnet (Recommended for Testing)
1. Visit [Binance Testnet](https://testnet.binance.vision/)
2. Create an account or login
3. Generate API keys from your account settings
4. Use these keys in your `.env` file with `USE_TESTNET=True`

### Live Trading
1. Visit [Binance](https://www.binance.com/)
2. Create an account and complete verification
3. Go to API Management in your account settings
4. Create API keys with trading permissions
5. **Enable IP whitelist for security**
6. Use these keys in your `.env` file with `USE_TESTNET=False`

## Safety & Best Practices

1. **Start with Testnet**: Always test your strategy on testnet first
2. **Backtest Thoroughly**: Run backtests on different time periods
3. **Start Small**: Begin with small amounts when going live
4. **Monitor Regularly**: Keep an eye on your bot's performance
5. **Risk Management**: Never risk more than you can afford to lose
6. **API Security**: 
   - Never share your API keys
   - Enable IP whitelist
   - Restrict API permissions to trading only (no withdrawals)

## Performance Metrics

The backtester calculates:
- **Total Trades**: Number of trades executed
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profits to gross losses
- **Max Drawdown**: Largest peak-to-trough decline
- **Total Return**: Overall percentage return
- **Average Win/Loss**: Average profit per winning/losing trade

## Disclaimer

**This trading bot is for educational purposes only. Cryptocurrency trading carries substantial risk of loss. Past performance does not guarantee future results. Only trade with money you can afford to lose. The authors are not responsible for any financial losses incurred through the use of this software.**

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
