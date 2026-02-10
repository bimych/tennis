# Trading Bot Quick Start Guide

This guide will help you get started building your trend-following trading bot in just a few steps.

## Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.9 or higher installed
- [ ] Git installed
- [ ] GitHub account
- [ ] VS Code with GitHub Copilot installed
- [ ] Basic understanding of Python
- [ ] Alpaca paper trading account (free): https://alpaca.markets/
- [ ] Alpha Vantage API key (free): https://www.alphavantage.co/support/#api-key

## Step-by-Step Getting Started

### Step 1: Set Up Your Project (5 minutes)

Create a new directory for your trading bot:

```bash
mkdir trading-bot
cd trading-bot
git init
```

### Step 2: Use Copilot Agent to Generate Structure (5 minutes)

Open VS Code in your project folder and use Copilot Chat:

**Prompt for Copilot:**
```
Create a Python trading bot project with this structure:
- src/bot/ (main trading logic)
- src/strategies/ (trading strategies)
- src/data/ (data fetching)
- src/backtest/ (backtesting engine)
- tests/ (unit tests)
- config/ (configuration files)
- Create requirements.txt with pandas, numpy, matplotlib, requests, python-dotenv, alpaca-trade-api, yfinance
- Create .gitignore for Python
- Create .env.example with placeholder for API keys
```

### Step 3: Install Dependencies (2 minutes)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables (2 minutes)

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
ALPACA_API_KEY=your_alpaca_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### Step 5: Create Your First Data Fetcher (10 minutes)

Use Copilot to create `src/data/data_fetcher.py`:

**Prompt for Copilot:**
```
Create a DataFetcher class in Python that:
1. Uses yfinance to fetch historical stock data
2. Takes symbol, start_date, end_date, and interval as parameters
3. Returns pandas DataFrame with OHLCV data
4. Has error handling for invalid symbols
5. Includes a main function to test fetching SPY data for the last year
```

Test it:
```bash
python src/data/data_fetcher.py
```

### Step 6: Create Simple Moving Average Strategy (15 minutes)

Use Copilot to create `src/strategies/simple_ma_strategy.py`:

**Prompt for Copilot:**
```
Create a SimpleMACrossStrategy class that:
1. Calculates 50-day and 200-day simple moving averages
2. Generates buy signal when 50-day MA crosses above 200-day MA (Golden Cross)
3. Generates sell signal when 50-day MA crosses below 200-day MA (Death Cross)
4. Takes a pandas DataFrame with 'close' column
5. Returns DataFrame with 'fast_ma', 'slow_ma', and 'signal' columns
6. Signal is 1 for buy, -1 for sell, 0 for hold
```

### Step 7: Create Simple Backtester (20 minutes)

Use Copilot to create `src/backtest/simple_backtester.py`:

**Prompt for Copilot:**
```
Create a SimpleBacktester class that:
1. Takes initial capital (default $10,000)
2. Takes historical data with signals
3. Simulates buying when signal is 1, selling when signal is -1
4. Tracks portfolio value over time
5. Calculates total return, max drawdown, and number of trades
6. Plots portfolio value over time using matplotlib
7. Includes commission of 0.1% per trade
```

### Step 8: Run Your First Backtest (5 minutes)

Create `run_backtest.py` in the root:

**Prompt for Copilot:**
```
Create a script that:
1. Uses DataFetcher to get SPY data for 2020-2024
2. Uses SimpleMACrossStrategy to generate signals
3. Uses SimpleBacktester to run backtest
4. Prints results and shows plot
```

Run it:
```bash
python run_backtest.py
```

You should see output like:
```
=== Backtest Results ===
Initial Capital: $10,000.00
Final Portfolio Value: $12,450.30
Total Return: 24.50%
Max Drawdown: -8.23%
Number of Trades: 8
```

## Next Steps

Once you've completed the quick start:

1. **Improve Your Strategy**:
   - Add more indicators (RSI, MACD, ADX)
   - Implement trend confirmation
   - Add stop losses and take profits

2. **Enhance Backtesting**:
   - Add more metrics (Sharpe ratio, win rate)
   - Test on multiple symbols
   - Implement walk-forward analysis

3. **Add Risk Management**:
   - Position sizing based on account value
   - Maximum drawdown limits
   - Portfolio heat management

4. **Paper Trading**:
   - Connect to Alpaca paper trading
   - Run strategy in real-time with fake money
   - Monitor performance for 1-2 months

5. **Read the Full Plan**:
   - See `TRADING_BOT_PLAN.md` for comprehensive guide
   - Follow Phase 1-7 for production-ready bot

## Copilot Tips for This Project

### Good Prompts:
✅ "Create a function that calculates RSI indicator from a pandas DataFrame"
✅ "Add error handling to this data fetcher for network timeouts"
✅ "Write unit tests for the moving average crossover strategy"
✅ "Optimize this backtester to run faster on large datasets"

### Avoid Vague Prompts:
❌ "Make my bot better"
❌ "Fix the code"
❌ "Add features"

### Use Copilot for:
- Writing boilerplate code quickly
- Implementing mathematical formulas (indicators)
- Creating test cases
- Adding error handling
- Writing documentation
- Refactoring code

## Common Issues & Solutions

### Issue: "Module not found" error
**Solution**: Make sure you're in the virtual environment and ran `pip install -r requirements.txt`

### Issue: API rate limit exceeded
**Solution**: Add delays between API calls or use cached data for testing

### Issue: Backtest shows unrealistic returns
**Solution**: Check for look-ahead bias, ensure you're using 'close' prices, add realistic commissions

### Issue: Strategy generates too many trades
**Solution**: Add trend confirmation filters or increase the moving average periods

## Resources

- **Full Plan**: See `TRADING_BOT_PLAN.md` for detailed roadmap
- **Alpaca Docs**: https://alpaca.markets/docs/
- **Pandas TA**: https://github.com/twopirllc/pandas-ta
- **Backtrader**: https://www.backtrader.com/ (alternative backtesting framework)

## Safety Reminders

⚠️ **This is for educational purposes**
- Start with paper trading only
- Never invest more than you can afford to lose
- Backtest thoroughly before going live
- Understand every line of code
- Past performance doesn't guarantee future results

Happy coding! 🚀
