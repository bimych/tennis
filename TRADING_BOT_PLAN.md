# Trading Bot Development Plan: 0 to 1
## Trend Following Strategy in Python

This document provides a comprehensive roadmap for building a trading bot from scratch using a trend-following strategy in Python, leveraging GitHub Copilot agents throughout the development process.

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Foundation Setup](#phase-1-foundation-setup)
4. [Phase 2: Data Infrastructure](#phase-2-data-infrastructure)
5. [Phase 3: Trend Following Strategy](#phase-3-trend-following-strategy)
6. [Phase 4: Backtesting Engine](#phase-4-backtesting-engine)
7. [Phase 5: Risk Management](#phase-5-risk-management)
8. [Phase 6: Live Trading Integration](#phase-6-live-trading-integration)
9. [Phase 7: Monitoring & Optimization](#phase-7-monitoring--optimization)
10. [Using Copilot Agents](#using-copilot-agents)

---

## Overview

### What is Trend Following?
Trend following is a trading strategy that attempts to capture gains through the analysis of an asset's momentum in a particular direction. The strategy is based on the premise that markets often move in trends, and profits can be made by identifying and following these trends.

### Key Principles:
- **Buy when price is trending up** (higher highs, higher lows)
- **Sell/Short when price is trending down** (lower highs, lower lows)
- **Cut losses quickly** when trend reverses
- **Let winners run** as long as trend continues

### Common Trend Following Indicators:
1. **Moving Averages (MA)** - Simple (SMA) and Exponential (EMA)
2. **Moving Average Convergence Divergence (MACD)**
3. **Average Directional Index (ADX)**
4. **Donchian Channels**
5. **Bollinger Bands**

---

## Prerequisites

### Required Knowledge:
- [ ] Python fundamentals (functions, classes, modules)
- [ ] Basic understanding of financial markets
- [ ] Git version control basics
- [ ] API concepts (REST APIs)

### Tools & Accounts Needed:
- [ ] Python 3.9+ installed
- [ ] Git installed
- [ ] GitHub account
- [ ] Code editor (VS Code recommended for Copilot)
- [ ] Trading platform account (Alpaca, Interactive Brokers, or Binance for crypto)
- [ ] Data provider access (Alpha Vantage, Yahoo Finance, or exchange APIs)

---

## Phase 1: Foundation Setup

### Step 1.1: Project Structure Setup
**Ask Copilot Agent to:**
```
Create a Python trading bot project structure with the following:
- src/bot/ for main bot code
- src/strategies/ for strategy implementations
- src/data/ for data fetching and storage
- src/backtest/ for backtesting engine
- tests/ for unit tests
- config/ for configuration files
- logs/ for logging
- Include .gitignore for Python projects
```

**Expected Directory Structure:**
```
trading-bot/
├── src/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── trader.py
│   │   └── executor.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py
│   │   └── trend_following.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py
│   │   └── data_processor.py
│   └── backtest/
│       ├── __init__.py
│       ├── backtester.py
│       └── metrics.py
├── tests/
├── config/
│   └── config.yaml
├── logs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Step 1.2: Dependencies Installation
**Ask Copilot Agent to:**
```
Create a requirements.txt file for a trading bot with:
- pandas for data manipulation
- numpy for numerical operations
- matplotlib and plotly for visualization
- requests for API calls
- python-dotenv for environment variables
- pyyaml for configuration
- pytest for testing
- ta-lib or pandas-ta for technical indicators
```

**Expected requirements.txt:**
```txt
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
plotly>=5.14.0
requests>=2.31.0
python-dotenv>=1.0.0
pyyaml>=6.0
pytest>=7.4.0
pandas-ta>=0.3.14b
alpaca-trade-api>=3.0.0  # or other broker SDK
yfinance>=0.2.28  # for free historical data
```

### Step 1.3: Configuration Setup
**Ask Copilot Agent to:**
```
Create a config.yaml template for trading bot with sections for:
- API credentials (placeholder)
- Trading parameters (symbols, timeframes)
- Strategy parameters (MA periods, thresholds)
- Risk management (max position size, stop loss)
- Backtesting parameters (start/end dates, initial capital)
```

---

## Phase 2: Data Infrastructure

### Step 2.1: Data Fetcher Implementation
**Ask Copilot Agent to:**
```
Create a DataFetcher class in src/data/data_fetcher.py that:
- Connects to Yahoo Finance or Alpha Vantage API
- Fetches historical OHLCV (Open, High, Low, Close, Volume) data
- Supports multiple timeframes (1m, 5m, 1h, 1d)
- Handles API rate limiting and errors gracefully
- Caches data locally to avoid redundant API calls
- Returns data as pandas DataFrame
```

**Key Methods:**
```python
class DataFetcher:
    def __init__(self, api_key: str = None)
    def fetch_historical_data(symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame
    def fetch_live_data(symbol: str, interval: str) -> pd.DataFrame
    def save_to_cache(data: pd.DataFrame, symbol: str, interval: str)
    def load_from_cache(symbol: str, interval: str) -> pd.DataFrame
```

### Step 2.2: Data Processor Implementation
**Ask Copilot Agent to:**
```
Create a DataProcessor class in src/data/data_processor.py that:
- Cleans and validates OHLCV data (removes NaN, checks for gaps)
- Resamples data to different timeframes
- Calculates technical indicators (SMA, EMA, MACD, RSI, ADX)
- Normalizes and scales data if needed
- Handles timezone conversions
```

**Key Methods:**
```python
class DataProcessor:
    def clean_data(df: pd.DataFrame) -> pd.DataFrame
    def resample_data(df: pd.DataFrame, target_interval: str) -> pd.DataFrame
    def add_moving_averages(df: pd.DataFrame, periods: List[int]) -> pd.DataFrame
    def add_macd(df: pd.DataFrame) -> pd.DataFrame
    def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame
    def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame
```

### Step 2.3: Testing Data Pipeline
**Ask Copilot Agent to:**
```
Create unit tests in tests/test_data.py that:
- Test data fetching for valid symbols
- Test error handling for invalid symbols
- Test data processing functions
- Test indicator calculations
- Mock API calls to avoid rate limits during testing
```

---

## Phase 3: Trend Following Strategy

### Step 3.1: Base Strategy Class
**Ask Copilot Agent to:**
```
Create an abstract BaseStrategy class in src/strategies/base_strategy.py that:
- Defines interface for all strategies
- Has methods: generate_signals(), calculate_position_size(), should_enter(), should_exit()
- Includes abstract methods that child classes must implement
- Stores strategy parameters
```

**Key Structure:**
```python
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, params: dict):
        self.params = params
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate buy/sell signals based on strategy logic"""
        pass
    
    @abstractmethod
    def should_enter(self, data: pd.DataFrame, index: int) -> str:
        """Returns 'long', 'short', or None"""
        pass
    
    @abstractmethod
    def should_exit(self, data: pd.DataFrame, index: int, position: str) -> bool:
        """Returns True if should exit current position"""
        pass
```

### Step 3.2: Trend Following Strategy Implementation
**Ask Copilot Agent to:**
```
Create a TrendFollowingStrategy class in src/strategies/trend_following.py that implements:

Strategy Logic:
1. Use dual moving average crossover (fast MA and slow MA)
   - Buy signal: When fast MA crosses above slow MA
   - Sell signal: When fast MA crosses below slow MA

2. Trend confirmation using ADX
   - Only enter trades when ADX > 25 (strong trend)
   
3. Entry rules:
   - Long: Fast MA > Slow MA AND ADX > 25 AND close > slow MA
   - Short: Fast MA < Slow MA AND ADX > 25 AND close < slow MA

4. Exit rules:
   - Exit long: Fast MA crosses below slow MA OR stop loss hit
   - Exit short: Fast MA crosses above slow MA OR stop loss hit

Include configurable parameters:
- fast_period (default: 50)
- slow_period (default: 200)
- adx_period (default: 14)
- adx_threshold (default: 25)
```

**Example Implementation Outline:**
```python
class TrendFollowingStrategy(BaseStrategy):
    def __init__(self, fast_period=50, slow_period=200, adx_threshold=25):
        params = {
            'fast_period': fast_period,
            'slow_period': slow_period,
            'adx_threshold': adx_threshold
        }
        super().__init__(params)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        # Calculate indicators
        data['fast_ma'] = data['close'].rolling(window=self.params['fast_period']).mean()
        data['slow_ma'] = data['close'].rolling(window=self.params['slow_period']).mean()
        data['adx'] = self.calculate_adx(data)
        
        # Generate signals
        data['signal'] = 0
        # Long signal
        data.loc[(data['fast_ma'] > data['slow_ma']) & 
                 (data['adx'] > self.params['adx_threshold']), 'signal'] = 1
        # Short signal
        data.loc[(data['fast_ma'] < data['slow_ma']) & 
                 (data['adx'] > self.params['adx_threshold']), 'signal'] = -1
        
        return data
    
    def calculate_adx(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        # ADX calculation implementation
        pass
```

### Step 3.3: Strategy Testing
**Ask Copilot Agent to:**
```
Create tests in tests/test_strategy.py that:
- Test signal generation with known data
- Test edge cases (insufficient data, all NaN values)
- Verify indicator calculations are correct
- Test strategy with different parameter combinations
```

---

## Phase 4: Backtesting Engine

### Step 4.1: Backtester Core Implementation
**Ask Copilot Agent to:**
```
Create a Backtester class in src/backtest/backtester.py that:
- Takes historical data and strategy as inputs
- Simulates trading based on strategy signals
- Tracks positions, PnL, and portfolio value over time
- Handles transaction costs (commissions, slippage)
- Supports both long and short positions
- Prevents look-ahead bias
- Returns detailed trade log and performance metrics
```

**Key Methods:**
```python
class Backtester:
    def __init__(self, initial_capital: float, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.trades = []
        self.portfolio_value = []
    
    def run(self, data: pd.DataFrame, strategy: BaseStrategy) -> dict:
        """Run backtest and return results"""
        pass
    
    def execute_trade(self, signal: int, price: float, timestamp: datetime):
        """Execute a trade based on signal"""
        pass
    
    def calculate_metrics(self) -> dict:
        """Calculate performance metrics"""
        pass
```

### Step 4.2: Performance Metrics Implementation
**Ask Copilot Agent to:**
```
Create a MetricsCalculator class in src/backtest/metrics.py that calculates:
- Total Return (%)
- Annualized Return (%)
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown (%)
- Win Rate (%)
- Profit Factor
- Average Win / Average Loss
- Number of trades
- Best/Worst trade
```

**Key Metrics:**
```python
class MetricsCalculator:
    @staticmethod
    def calculate_returns(portfolio_values: pd.Series) -> float:
        """Calculate total return"""
        pass
    
    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        pass
    
    @staticmethod
    def calculate_max_drawdown(portfolio_values: pd.Series) -> float:
        """Calculate maximum drawdown"""
        pass
    
    @staticmethod
    def calculate_all_metrics(trades: List[dict], portfolio_values: pd.Series) -> dict:
        """Calculate all performance metrics"""
        pass
```

### Step 4.3: Visualization
**Ask Copilot Agent to:**
```
Create a visualization module in src/backtest/visualizer.py that:
- Plots portfolio value over time
- Plots equity curve with drawdown
- Plots buy/sell signals on price chart
- Creates candlestick charts with indicators
- Generates performance reports (PDF or HTML)
```

---

## Phase 5: Risk Management

### Step 5.1: Position Sizing
**Ask Copilot Agent to:**
```
Create a RiskManager class in src/bot/risk_manager.py that implements:
- Fixed fractional position sizing (e.g., 2% of capital per trade)
- Kelly Criterion position sizing
- ATR-based position sizing
- Maximum position size limits
- Portfolio heat management (total risk across all positions)
```

**Key Methods:**
```python
class RiskManager:
    def __init__(self, max_risk_per_trade: float = 0.02, max_portfolio_risk: float = 0.06):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_risk = max_portfolio_risk
    
    def calculate_position_size(self, capital: float, entry_price: float, 
                                stop_loss: float, method: str = 'fixed') -> int:
        """Calculate number of shares/contracts to buy"""
        pass
    
    def can_open_position(self, current_positions: List[dict]) -> bool:
        """Check if portfolio risk allows new position"""
        pass
```

### Step 5.2: Stop Loss & Take Profit
**Ask Copilot Agent to:**
```
Implement stop loss and take profit logic:
- ATR-based stop loss (e.g., 2x ATR below entry)
- Percentage-based stop loss (e.g., 2% below entry)
- Trailing stop loss (follows price as it moves favorably)
- Take profit at risk/reward ratio (e.g., 1:2 or 1:3)
```

---

## Phase 6: Live Trading Integration

### Step 6.1: Broker Connection
**Ask Copilot Agent to:**
```
Create a BrokerConnector class in src/bot/broker.py that:
- Connects to broker API (Alpaca, Interactive Brokers, etc.)
- Authenticates using API keys from environment variables
- Fetches account information (balance, positions)
- Places market and limit orders
- Cancels orders
- Handles API errors and rate limits
```

**For Alpaca (paper trading recommended initially):**
```python
import alpaca_trade_api as tradeapi

class AlpacaBroker:
    def __init__(self, api_key: str, secret_key: str, base_url: str):
        self.api = tradeapi.REST(api_key, secret_key, base_url)
    
    def get_account(self) -> dict:
        """Get account information"""
        pass
    
    def place_order(self, symbol: str, qty: int, side: str, 
                    order_type: str = 'market') -> dict:
        """Place an order"""
        pass
    
    def get_positions(self) -> List[dict]:
        """Get current positions"""
        pass
```

### Step 6.2: Trading Bot Main Loop
**Ask Copilot Agent to:**
```
Create the main TradingBot class in src/bot/trader.py that:
- Runs in a continuous loop
- Fetches latest market data at specified intervals
- Generates signals using the strategy
- Executes trades via broker API
- Manages open positions
- Logs all activities
- Handles exceptions gracefully
- Has start/stop mechanisms
```

**Main Bot Structure:**
```python
class TradingBot:
    def __init__(self, strategy: BaseStrategy, broker: BrokerConnector, 
                 risk_manager: RiskManager, config: dict):
        self.strategy = strategy
        self.broker = broker
        self.risk_manager = risk_manager
        self.config = config
        self.running = False
    
    def start(self):
        """Start the trading bot"""
        self.running = True
        while self.running:
            try:
                self.execute_trading_cycle()
                time.sleep(self.config['check_interval'])
            except Exception as e:
                logging.error(f"Error in trading cycle: {e}")
    
    def execute_trading_cycle(self):
        """One iteration of the trading loop"""
        # 1. Fetch latest data
        # 2. Generate signals
        # 3. Check risk limits
        # 4. Execute trades if signals present
        # 5. Update positions
        pass
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
```

### Step 6.3: Logging and Monitoring
**Ask Copilot Agent to:**
```
Set up comprehensive logging in src/bot/logger.py:
- Log all trades (entry, exit, PnL)
- Log errors and exceptions
- Log daily performance summary
- Save logs to files with rotation
- Optional: Send alerts via email/Telegram
```

---

## Phase 7: Monitoring & Optimization

### Step 7.1: Performance Dashboard
**Ask Copilot Agent to:**
```
Create a simple web dashboard using Flask or Streamlit that displays:
- Current portfolio value
- Open positions
- Recent trades
- Daily/weekly/monthly performance
- Strategy parameters
- Real-time charts
```

### Step 7.2: Strategy Optimization
**Ask Copilot Agent to:**
```
Create a parameter optimization script in src/optimization/optimizer.py that:
- Tests strategy with different parameter combinations
- Uses grid search or random search
- Evaluates each combination on historical data
- Ranks results by Sharpe ratio or other metrics
- Saves best parameters to config
- Includes walk-forward analysis to prevent overfitting
```

### Step 7.3: Paper Trading Testing
**Before going live:**
1. Test on paper trading for at least 1-2 months
2. Monitor all trades and verify logic is correct
3. Check for any bugs or unexpected behavior
4. Validate risk management is working properly
5. Review logs daily

---

## Using Copilot Agents

### How to Use GitHub Copilot Agents Effectively

#### 1. **Start with Structure**
Ask agent to create the entire project structure first:
```
"Create a complete Python trading bot project structure with all necessary folders and files"
```

#### 2. **Implement One Module at a Time**
Break down into small, focused requests:
```
"Implement the DataFetcher class that fetches stock data from Yahoo Finance API"
```

#### 3. **Request Tests Alongside Code**
Always ask for tests:
```
"Create the TrendFollowingStrategy class with unit tests"
```

#### 4. **Use Agents for Different Phases**
- **Code Agent**: For implementation
- **Test Agent**: For writing comprehensive tests
- **Review Agent**: For code review and optimization
- **Documentation Agent**: For creating documentation

#### 5. **Iterative Development**
Build incrementally:
```
Phase 1: "Create basic data fetcher"
Phase 2: "Add caching to data fetcher"
Phase 3: "Add error handling to data fetcher"
```

#### 6. **Ask for Explanations**
Request explanations for complex logic:
```
"Explain how the ADX indicator is calculated in this strategy"
```

#### 7. **Request Improvements**
Ask agents to optimize:
```
"Review this backtester code and suggest performance improvements"
```

### Copilot Agent Workflow for This Project

```
Session 1: Setup
→ "Create trading bot project structure"
→ "Create requirements.txt with all dependencies"
→ "Set up configuration system with YAML"

Session 2: Data Infrastructure  
→ "Implement DataFetcher class for Yahoo Finance"
→ "Create DataProcessor with technical indicators"
→ "Write tests for data pipeline"

Session 3: Strategy
→ "Create BaseStrategy abstract class"
→ "Implement TrendFollowingStrategy with dual MA and ADX"
→ "Write unit tests for strategy"

Session 4: Backtesting
→ "Create Backtester class with position tracking"
→ "Implement performance metrics calculator"
→ "Add visualization for backtest results"

Session 5: Risk Management
→ "Implement RiskManager with position sizing"
→ "Add stop loss and take profit logic"
→ "Test risk management with edge cases"

Session 6: Live Trading (Paper)
→ "Create broker connector for Alpaca"
→ "Implement main TradingBot loop"
→ "Set up logging system"

Session 7: Testing & Deployment
→ "Run complete end-to-end test"
→ "Create deployment documentation"
→ "Set up monitoring dashboard"
```

---

## Next Steps

### Immediate Actions:
1. ✅ Review this plan thoroughly
2. ⬜ Set up development environment (Python, VS Code, GitHub Copilot)
3. ⬜ Create trading/investment account (Alpaca paper trading recommended)
4. ⬜ Get API keys for data provider
5. ⬜ Start with Phase 1 using Copilot agents

### Learning Resources:
- **Trend Following Books**: "Following the Trend" by Andreas Clenow
- **Python for Trading**: "Python for Finance" by Yves Hilpisch
- **Backtesting**: QuantConnect and Backtrader documentation
- **Risk Management**: "Trade Your Way to Financial Freedom" by Van Tharp

### Important Warnings:
⚠️ **NEVER trade real money until:**
- You have thoroughly backtested your strategy on at least 2-3 years of data
- You have paper traded successfully for at least 1-2 months
- You understand every line of code in your bot
- You have proper risk management in place
- You can afford to lose the money you're trading with

⚠️ **Common Pitfalls to Avoid:**
- Over-optimization (curve fitting)
- Look-ahead bias in backtesting
- Ignoring transaction costs
- Poor risk management
- Trading with money you can't afford to lose
- Not testing in paper trading first

---

## Summary

This plan takes you from zero to a fully functional trend-following trading bot:

1. **Foundation**: Project structure, dependencies, configuration
2. **Data**: Fetching and processing market data
3. **Strategy**: Implementing trend following logic
4. **Backtesting**: Testing strategy on historical data
5. **Risk Management**: Position sizing and stop losses
6. **Live Trading**: Connecting to broker and executing trades
7. **Monitoring**: Dashboard and optimization

**Estimated Timeline**: 4-8 weeks (depending on experience and time commitment)
- Week 1-2: Foundation + Data Infrastructure
- Week 3-4: Strategy + Backtesting
- Week 5-6: Risk Management + Live Integration
- Week 7-8: Testing + Optimization

**Use Copilot agents at every step** to speed up development and learn best practices.

Good luck with your trading bot! 🚀📈
