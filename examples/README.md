# Trading Bot Examples

This directory contains working code examples to help you get started building your trading bot.

## Examples Included

### 1. `example_data_fetcher.py`
Demonstrates how to fetch historical stock data using Yahoo Finance.

**Features:**
- Fetch historical OHLCV data for any symbol
- Fetch recent data for quick analysis
- Error handling for invalid symbols
- Returns data as pandas DataFrames

**Run it:**
```bash
cd examples
python example_data_fetcher.py
```

### 2. `example_strategy.py`
Implements a simple moving average crossover strategy.

**Features:**
- Calculates 50-day and 200-day moving averages
- Generates buy/sell signals on crossovers
- Visualizes strategy signals on price chart
- Shows position over time

**Run it:**
```bash
cd examples
python example_strategy.py
```

### 3. `example_backtester.py`
A complete backtesting engine to test your strategies.

**Features:**
- Simulates trading based on signals
- Tracks portfolio value over time
- Calculates performance metrics (return, drawdown, Sharpe ratio, win rate)
- Visualizes backtest results
- Handles transaction costs

**Run it:**
```bash
cd examples
python example_backtester.py
```

## Installation

Install required dependencies:

```bash
pip install pandas numpy matplotlib yfinance
```

Or use the provided requirements file:

```bash
pip install -r example_requirements.txt
```

## How to Use These Examples

### Quick Start (5 minutes)

1. **Test the data fetcher:**
   ```bash
   python example_data_fetcher.py
   ```
   This will fetch SPY data and display basic statistics.

2. **Run the strategy:**
   ```bash
   python example_strategy.py
   ```
   This will generate signals and create a chart showing buy/sell points.

3. **Run a full backtest:**
   ```bash
   python example_backtester.py
   ```
   This will run a complete backtest and show performance metrics.

### Modify and Experiment

Try changing these parameters to see different results:

**In `example_strategy.py`:**
```python
# Change the moving average periods
strategy = SimpleMACrossStrategy(fast_period=20, slow_period=50)  # Faster signals
strategy = SimpleMACrossStrategy(fast_period=100, slow_period=300)  # Slower signals
```

**In `example_backtester.py`:**
```python
# Change initial capital and commission
backtester = SimpleBacktester(initial_capital=50000, commission=0.002)
```

**In `example_data_fetcher.py`:**
```python
# Try different symbols and date ranges
data = fetcher.fetch_historical_data('AAPL', '2020-01-01', '2024-01-01')
data = fetcher.fetch_historical_data('TSLA', '2019-01-01', '2024-01-01')
```

## Expected Output

### Data Fetcher Output:
```
=== Data Fetcher Example ===

Fetching SPY data for 2023...
Fetched 251 rows of data

First 5 rows:
                  open    high     low   close      volume
Date                                                       
2023-01-03  384.53  386.87  383.03  384.16  112117500
...

Basic statistics:
count    251.000000
mean     432.453187
std       23.891234
...
```

### Strategy Output:
```
=== Simple MA Crossover Strategy Example ===

Strategy Statistics:
  Buy Signals: 3
  Sell Signals: 3
  Time in Market: 62.15%
  Long Periods: 124
  Flat Periods: 76

Chart saved to /tmp/strategy_example.png
```

### Backtester Output:
```
==================================================
BACKTEST RESULTS
==================================================
Initial Capital:        $10,000.00
Final Portfolio Value:  $12,450.30
Total Return:           24.50%
Max Drawdown:           -8.23%
Sharpe Ratio:           1.45

Number of Trades:       8
Winning Trades:         5
Losing Trades:          3
Win Rate:               62.50%
==================================================
```

## Next Steps

After running these examples:

1. **Understand the code**: Read through each file and understand what it does
2. **Experiment**: Modify parameters and see how results change
3. **Combine**: Use these as building blocks for your own trading bot
4. **Enhance**: Add more indicators, better risk management, etc.
5. **Read the full plan**: See `../TRADING_BOT_PLAN.md` for comprehensive guide

## Common Issues

### Issue: Module not found
**Solution**: Install dependencies with `pip install pandas numpy matplotlib yfinance`

### Issue: No data fetched
**Solution**: Check your internet connection and try a different symbol

### Issue: Plots don't show
**Solution**: The plots are saved to `/tmp/`. Check there if they don't display.

## Using with Copilot

You can use these examples as reference when asking Copilot to generate code:

```
"Create a strategy similar to example_strategy.py but using RSI instead of moving averages"

"Enhance example_backtester.py to support short selling"

"Add position sizing based on volatility to example_backtester.py"
```

## Resources

- **Yahoo Finance API**: https://pypi.org/project/yfinance/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Technical Analysis Library**: https://technical-analysis-library-in-python.readthedocs.io/

Happy trading! 📈
