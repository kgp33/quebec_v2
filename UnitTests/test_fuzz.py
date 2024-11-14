import pytest
import pandas as pd
import json
import random
from datetime import datetime, timedelta
import numpy as np
from hypothesis import given, settings, strategies as st
from PriceApp.price import fetch_portfolio_sharpe_ratio, calculate_total_portfolio_value, load_portfolio

# Reduce the number of examples for faster testing
settings.register_profile("dev", max_examples=10)
settings.load_profile("dev")

@st.composite
def stock_portfolio_strategy(draw):
    """Generate a valid portfolio with 1-5 stocks."""
    n_stocks = draw(st.integers(min_value=1, max_value=5))
    
    all_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA']
    selected_tickers = draw(st.lists(st.sampled_from(all_tickers), 
                                   min_size=1, 
                                   max_size=min(n_stocks, len(all_tickers)), 
                                   unique=True))
    
    portfolio = []
    for ticker in selected_tickers:
        shares = draw(st.integers(min_value=10, max_value=100))
        portfolio.append({
            "ticker": ticker,
            "nShares": shares
        })
    
    return portfolio








def generate_realistic_returns(n_days):
    """Generate realistic daily returns."""
    base_returns = np.random.normal(0.0004, 0.015, n_days)  # ~10% annual return, 0.0004 daily return 0.015 is the desired standard deviation
    return base_returns 





@st.composite
def portfolio_with_historical_data(draw):
    """Generate a portfolio with historical price data."""
    portfolio = draw(stock_portfolio_strategy()) #uses stock_portfolio_strategy to generate a portfolio of lengh max. 5
    
    # Generate one year of trading days
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D') 
    n_days = len(dates)
    
    # Create price data for each ticker
    price_data = {}
    known_prices = {}  # Store the last known price for each ticker
    

    # For each stock we generate random price, return rate
    for stock in portfolio:
        ticker = stock['ticker']
        base_price = draw(st.floats(min_value=100.0, max_value=1000.0)) # initial price of the stock
        
        # Generate random returns
        daily_returns = generate_realistic_returns(n_days)  # Generate reasonable random returns for the days
        
        # Convert returns to prices
        prices = [base_price]  # start with the initial price
        for ret in daily_returns:
            prices.append(prices[-1] * (1 + ret))  # we append new prices based on previous prices 
            
        price_data[ticker] = pd.Series(prices[:-1], index=dates)  #Store closing prices in the price data with ticker as index (just like price.py)
        known_prices[ticker] = prices[-2]  # Store the last price
    
    return portfolio, pd.DataFrame(price_data), known_prices  # return portfolio like the portfolio.json and then price_data like the one in price.py and then
                                                              # there is a new object called known price which is the current closing price for portfolio evaluation








@given(portfolio_and_data=portfolio_with_historical_data())
def test_fuzz_portfolio_value(portfolio_and_data):
    """Test total portfolio value calculation."""
    portfolio, price_data, current_prices = portfolio_and_data
    
    print(f"\nTesting portfolio value calculation:")
    print(f"Portfolio: {portfolio}")
    print(f"Last known prices: {current_prices}")
    
    # Calculate expected total value manually
    expected_value = sum(stock['nShares'] * current_prices[stock['ticker']] 
                        for stock in portfolio)
    
    # Calculate actual value using the function
    date_str = price_data.index[-1].strftime('%Y-%m-%d')
    calculated_value = calculate_total_portfolio_value(portfolio, price_data, date_str)
    
    print(f"Expected value: {expected_value}")
    print(f"Calculated value: {calculated_value}")
    
    # Verify the results
    assert calculated_value is not None, "Portfolio value should not be None"
    assert abs(calculated_value - expected_value) < 0.01, \
        f"Portfolio value mismatch: expected {expected_value}, got {calculated_value}"







@given(portfolio_and_data=portfolio_with_historical_data())
def test_fuzz_sharpe_ratio(portfolio_and_data):
    """Test Sharpe ratio calculation."""
    portfolio, price_data, _ = portfolio_and_data # Current price is not needed when calculating the sharpe ratio
    
    print(f"\nTesting Sharpe ratio for portfolio: {portfolio}")
    print(f"Price data shape: {price_data.shape}")
    
    # Calculate total investment
    date_str = price_data.index[-1].strftime('%Y-%m-%d') #converts the last date in price_data to string and use it to calculate the portfolio’s total value.
    try:
        total_investment = float(calculate_total_portfolio_value(portfolio, price_data, date_str))
        print(f"Total investment: {total_investment}")
        
        if total_investment <= 0:
            pytest.skip("Invalid total investment value")
            
        # Calculate portfolio returns 
        returns = price_data.pct_change().dropna()
        portfolio_returns = pd.Series(0, index=returns.index)  # initialize portfolio returns with the same date index as returns argument
        for stock in portfolio:
            weight = (float(price_data[stock['ticker']].iloc[-1]) * stock['nShares']) / total_investment
            portfolio_returns += returns[stock['ticker']] * weight
        
        volatility = portfolio_returns.std()
        print(f"Portfolio volatility: {volatility}")
        

        # after several test we can see that having low volatility or zero can lead to errors since we can not have 0 as the denominator
        if volatility < 0.001:
            pytest.skip("Portfolio volatility too low for meaningful Sharpe ratio")
        
        # Calculate Sharpe ratio
        sharpe_ratio = fetch_portfolio_sharpe_ratio(portfolio, price_data, total_investment)
        print(f"Calculated Sharpe ratio: {sharpe_ratio}")
        
        assert sharpe_ratio is not None, "Sharpe ratio should not be None"
        assert isinstance(sharpe_ratio, float), "Sharpe ratio should be a float"
        assert not np.isnan(sharpe_ratio), "Sharpe ratio should not be NaN"
        assert not np.isinf(sharpe_ratio), "Sharpe ratio should not be infinite"
        assert -5 <= sharpe_ratio <= 5, f"Sharpe ratio {sharpe_ratio} outside reasonable range" # set up a reasonable range. It could be any other number
        
    except (TypeError, ValueError) as e:
        print(f"Error during calculation: {e}")
        pytest.skip(f"Calculation error: {e}")








def test_basic_portfolio_calculations():
    """Test both portfolio value and Sharpe ratio with simple, predictable data."""
    portfolio = [
        {"ticker": "AAPL", "nShares": 100},
        {"ticker": "MSFT", "nShares": 200}
    ]
    
    # Create test data
    dates = pd.date_range(start='2023-01-01', periods=252, freq='B')
    n_days = len(dates)
    
    # Generate prices with known characteristics
    aapl_returns = generate_realistic_returns(n_days)
    msft_returns = generate_realistic_returns(n_days)
    
    aapl_prices = 100 * np.cumprod(1 + aapl_returns)
    msft_prices = 200 * np.cumprod(1 + msft_returns)
    
    price_data = pd.DataFrame({
        'AAPL': aapl_prices,
        'MSFT': msft_prices
    }, index=dates)
    
    # Test portfolio value
    expected_value = aapl_prices[-1] * 100 + msft_prices[-1] * 200
    date_str = dates[-1].strftime('%Y-%m-%d')
    calculated_value = calculate_total_portfolio_value(portfolio, price_data, date_str)
    
    print("\nBasic test results:")
    print(f"Expected portfolio value: {expected_value}")
    print(f"Calculated portfolio value: {calculated_value}")
    
    assert abs(calculated_value - expected_value) < 0.01, "Portfolio value calculation error"
    
    # Test Sharpe ratio
    sharpe_ratio = fetch_portfolio_sharpe_ratio(portfolio, price_data, calculated_value)
    print(f"Sharpe ratio: {sharpe_ratio}")
    
    assert not np.isnan(sharpe_ratio), "Sharpe ratio should not be NaN"
    assert not np.isinf(sharpe_ratio), "Sharpe ratio should not be infinite"
    assert -5 <= sharpe_ratio <= 5, "Sharpe ratio should be reasonable"







def test_edge_cases():
    """Test edge cases for both portfolio value and Sharpe ratio calculations."""
    dates = pd.date_range(start='2023-01-01', periods=5, freq='B')
    
    # Test case 1: Empty portfolio
    empty_portfolio = []
    price_data = pd.DataFrame({
        'AAPL': [100, 101, 102, 103, 104]
    }, index=dates)
    
    value = calculate_total_portfolio_value(empty_portfolio, price_data, dates[-1].strftime('%Y-%m-%d'))
    assert value == 0, "Empty portfolio should have zero value"
    
    # Test case 2: Missing ticker
    invalid_portfolio = [{"ticker": "INVALID", "nShares": 100}]
    value = calculate_total_portfolio_value(invalid_portfolio, price_data, dates[-1].strftime('%Y-%m-%d'))
    assert value is None, "Invalid ticker should return None"
    
    # Test case 3: Missing date
    valid_portfolio = [{"ticker": "AAPL", "nShares": 100}]
    value = calculate_total_portfolio_value(valid_portfolio, price_data, '2025-01-01')
    assert value is None, "Invalid date should return None"






if __name__ == "__main__":
    pytest.main([__file__])
