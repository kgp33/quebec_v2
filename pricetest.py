import json
from datetime import datetime
from price import fetch_portfolio_sharpe_ratio, load_portfolio, calculate_total_portfolio_value

def test_fetch_portfolio_sharpe_ratio():
    """
    Test the fetch_portfolio_sharpe_ratio function against an expected value.
    """
    
    # Load the portfolio JSON
    portfolio_file = 'portfolio.json'
    portfolio_data = load_portfolio(portfolio_file)

    # Define the expected Sharpe Ratio and tolerance
    expected_sharpe_ratio = 0.137  # Replace this with your expected value
    tolerance = 0.01  # Adjust the tolerance level if needed
    
    # Test the fetch_portfolio_sharpe_ratio function
    calculated_sharpe_ratio = fetch_portfolio_sharpe_ratio(portfolio_data)

    # Use pytest's assert for validation
    assert calculated_sharpe_ratio is not None, "Failed to calculate Sharpe Ratio." #nosec
    assert abs(calculated_sharpe_ratio - expected_sharpe_ratio) <= tolerance, \
        f"Test failed: The calculated Sharpe Ratio {calculated_sharpe_ratio} is not equal to the expected value {expected_sharpe_ratio}." #nosec




def test_calculate_total_portfolio_value():

    """
    Test the calculate_total_portfolio_value function against an expected value.
    """

    # Load the portfolio JSON
    portfolio_file = 'portfolio.json'
    portfolio_data = load_portfolio(portfolio_file)


    # Expected value of the function
    expected_portfolio_value = float(24808.70)

    # Set up tolerance level for differences between actual and expected value
    tolerance = 0.01

    # Test the portfolio value function
    calculated_total_portfolio_value = calculate_total_portfolio_value(portfolio_data)

    assert calculated_total_portfolio_value is not None, "Failed to calculate Portfolio Value" #nosec
    assert abs(calculated_total_portfolio_value - expected_portfolio_value) <= tolerance, \
        f"Test failed: The calculated Portfolio Value {calculated_total_portfolio_value} is not equal to the expected value {expected_portfolio_value}." #nosec

if __name__ == "__main__":
    # For running standalone, outside of pytest
    print(f"Running test on {datetime.today().strftime('%Y-%m-%d')}")
    test_fetch_portfolio_sharpe_ratio()
    test_calculate_total_portfolio_value()
