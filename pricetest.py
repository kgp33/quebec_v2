import pandas as pd
from datetime import datetime
from price import fetch_portfolio_sharpe_ratio, load_portfolio, calculate_total_portfolio_value
import pytest

@pytest.fixture
def price_data():
    return pd.read_json('test_data.json')


def test_calculate_total_portfolio_value(price_data):

    """
    Test the calculate_total_portfolio_value function against an expected value.
    """

    # Load the portfolio JSON
    portfolio_file = 'portfolio.json'
    portfolio_data = load_portfolio(portfolio_file)


    # Expected value of the function
    expected_portfolio_value = float(24231.70)

    # Set up tolerance level for differences between actual and expected value
    tolerance = 0.01

    # Test the portfolio value function
    calculated_total_portfolio_value = calculate_total_portfolio_value(portfolio_data, price_data, '2024-11-04')

    assert calculated_total_portfolio_value is not None, "Failed to calculate Portfolio Value"
    assert abs(calculated_total_portfolio_value - expected_portfolio_value) <= tolerance, \
        f"Test failed: The calculated Portfolio Value {calculated_total_portfolio_value} is not equal to the expected value {expected_portfolio_value}."


def test_fetch_portfolio_sharpe_ratio(price_data):
    """
    Test the fetch_portfolio_sharpe_ratio function against an expected value.
    """

    # Load the portfolio JSON
    portfolio_file = 'portfolio.json'
    portfolio_data = load_portfolio(portfolio_file)
    total_investment = calculate_total_portfolio_value(portfolio_data, price_data, '2024-11-04')

    # Define the expected Sharpe Ratio and tolerance
    expected_sharpe_ratio = 0.109  # Replace this with your expected value
    tolerance = 0.001  # Adjust the tolerance level if needed
    
    # Test the fetch_portfolio_sharpe_ratio function
    calculated_sharpe_ratio = fetch_portfolio_sharpe_ratio(portfolio_data, price_data, total_investment)

    # Use pytest's assert for validation
    assert calculated_sharpe_ratio is not None, "Failed to calculate Sharpe Ratio."
    assert abs(calculated_sharpe_ratio - expected_sharpe_ratio) <= tolerance, \
        f"Test failed: The calculated Sharpe Ratio {calculated_sharpe_ratio} is not equal to the expected value {expected_sharpe_ratio}."
