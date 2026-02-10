#!/usr/bin/env python3
"""
Simple tests to verify trading bot components.
"""
import pandas as pd
import numpy as np
from trading_bot.indicators import Indicators
from trading_bot.demo_data import DemoDataGenerator
from trading_bot.strategy import TradingStrategy, Position
from trading_bot.risk_manager import RiskManager
from datetime import datetime


def test_ema_calculation():
    """Test EMA calculation."""
    print("Testing EMA calculation...")
    
    # Create simple test data
    data = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='h'),
        'open': [100 + i for i in range(100)],
        'high': [101 + i for i in range(100)],
        'low': [99 + i for i in range(100)],
        'close': [100 + i for i in range(100)],
        'volume': [1000] * 100
    })
    
    # Add EMAs
    data = Indicators.add_emas(data, 20, 50)
    
    # Verify EMAs are calculated
    assert 'ema_short' in data.columns, "EMA short not calculated"
    assert 'ema_long' in data.columns, "EMA long not calculated"
    assert not data['ema_short'].isna().all(), "EMA short all NaN"
    assert not data['ema_long'].isna().all(), "EMA long all NaN"
    
    # EMA should generally follow the trend
    assert data['ema_short'].iloc[-1] > data['ema_short'].iloc[20], "EMA should trend upward"
    
    print("✓ EMA calculation test passed")


def test_uptrend_detection():
    """Test uptrend detection."""
    print("Testing uptrend detection...")
    
    # Test clear uptrend
    assert Indicators.is_uptrend(110, 100) == True, "Should detect uptrend"
    assert Indicators.is_uptrend(100, 110) == False, "Should not detect uptrend"
    assert Indicators.is_uptrend(100, 100) == False, "Equal EMAs should not be uptrend"
    
    print("✓ Uptrend detection test passed")


def test_price_near_ema():
    """Test price near EMA check."""
    print("Testing price near EMA...")
    
    # Price exactly on EMA
    assert Indicators.is_price_near_ema(100, 100, 0.01) == True
    
    # Price within 1% above
    assert Indicators.is_price_near_ema(100.5, 100, 0.01) == True
    
    # Price within 1% below
    assert Indicators.is_price_near_ema(99.5, 100, 0.01) == True
    
    # Price outside 1% range
    assert Indicators.is_price_near_ema(102, 100, 0.01) == False
    assert Indicators.is_price_near_ema(98, 100, 0.01) == False
    
    print("✓ Price near EMA test passed")


def test_position_class():
    """Test Position class."""
    print("Testing Position class...")
    
    # Create a position
    pos = Position(
        entry_price=50000,
        quantity=0.1,
        stop_loss=49000,
        take_profit=52000,
        entry_time=datetime.now()
    )
    
    # Test should_exit with stop loss
    should_exit, reason = pos.should_exit(48900)
    assert should_exit == True, "Should exit on stop loss"
    assert reason == "Stop Loss", "Reason should be Stop Loss"
    
    # Test should_exit with take profit
    should_exit, reason = pos.should_exit(52100)
    assert should_exit == True, "Should exit on take profit"
    assert reason == "Take Profit", "Reason should be Take Profit"
    
    # Test no exit
    should_exit, reason = pos.should_exit(50500)
    assert should_exit == False, "Should not exit"
    
    # Test PnL calculation
    pnl = pos.get_pnl(51000)
    expected_pnl = (51000 - 50000) * 0.1
    assert abs(pnl - expected_pnl) < 0.01, f"PnL calculation wrong: {pnl} vs {expected_pnl}"
    
    print("✓ Position class test passed")


def test_trailing_stop():
    """Test trailing stop functionality."""
    print("Testing trailing stop...")
    
    pos = Position(
        entry_price=50000,
        quantity=0.1,
        stop_loss=49000,
        take_profit=52000,
        entry_time=datetime.now()
    )
    
    # Initially not in profit, trailing stop should not activate
    pos.update_trailing_stop(49500, 0.01)
    assert pos.trailing_stop_active == False, "Trailing stop should not activate when not in profit"
    
    # Price goes up, trailing stop should activate
    pos.update_trailing_stop(51000, 0.01)
    assert pos.trailing_stop_active == True, "Trailing stop should activate when in profit"
    expected_stop = 51000 * 0.99
    assert abs(pos.stop_loss - expected_stop) < 1, f"Trailing stop not updated correctly: {pos.stop_loss} vs {expected_stop}"
    
    # Price goes higher, stop should move up
    old_stop = pos.stop_loss
    pos.update_trailing_stop(52000, 0.01)
    assert pos.stop_loss > old_stop, "Trailing stop should move up with price"
    
    # Price goes down, stop should not move down
    pos.update_trailing_stop(51000, 0.01)
    assert pos.stop_loss > 51000 * 0.99, "Trailing stop should not move down"
    
    print("✓ Trailing stop test passed")


def test_risk_manager():
    """Test risk management."""
    print("Testing risk manager...")
    
    rm = RiskManager(initial_balance=10000)
    
    # Test initial state
    assert rm.current_balance == 10000, "Initial balance wrong"
    assert rm.can_trade()[0] == True, "Should be able to trade initially"
    
    # Test daily loss limit
    rm.update_balance(-300, datetime.now())  # 3% loss
    can_trade, reason = rm.can_trade()
    assert can_trade == False, "Should halt trading after 3% loss"
    assert "Daily loss limit" in reason, "Reason should mention daily loss limit"
    
    print("✓ Risk manager test passed")


def test_demo_data_generation():
    """Test demo data generation."""
    print("Testing demo data generation...")
    
    df = DemoDataGenerator.generate_demo_data(
        start_price=50000,
        num_candles=100,
        volatility=0.02
    )
    
    assert len(df) == 100, "Wrong number of candles"
    assert all(col in df.columns for col in ['timestamp', 'open', 'high', 'low', 'close', 'volume']), "Missing columns"
    
    # Verify OHLC logic (high >= open, close; low <= open, close)
    for idx, row in df.iterrows():
        assert row['high'] >= row['open'], f"High should be >= open at index {idx}"
        assert row['high'] >= row['close'], f"High should be >= close at index {idx}"
        assert row['low'] <= row['open'], f"Low should be <= open at index {idx}"
        assert row['low'] <= row['close'], f"Low should be <= close at index {idx}"
    
    print("✓ Demo data generation test passed")


def main():
    """Run all tests."""
    print("="*60)
    print("RUNNING TRADING BOT TESTS")
    print("="*60 + "\n")
    
    try:
        test_ema_calculation()
        test_uptrend_detection()
        test_price_near_ema()
        test_position_class()
        test_trailing_stop()
        test_risk_manager()
        test_demo_data_generation()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
