import yfinance as yf
from datetime import datetime, timedelta
import json


def get_historical_stock_price(ticker, purchase_date):
    """
    Fetches the closing stock price on the specified purchase date.

    Parameters:
        ticker (str): The stock ticker symbol.
        purchase_date (str): The date of purchase in 'YYYY-MM-DD' format.

    Returns:
        float: The closing price on the purchase date, or None if no data is available.
    """
    stock = yf.Ticker(ticker)
    purchase_date_dt = datetime.strptime(purchase_date, '%Y-%m-%d')

    hist = stock.history(start=purchase_date_dt,
                         end=purchase_date_dt + timedelta(days=1), interval="1d")

    if not hist.empty:
        price_at_purchase = hist['Close'].iloc[0]
    else:
        price_at_purchase = None

    return price_at_purchase


def get_current_stock_price(ticker):
    """
    Fetches the latest available closing stock price.

    Parameters:
        ticker (str): The stock ticker symbol.

    Returns:
        float: The most recent closing price of the stock.
    """
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    return current_price


def calculate_investment_value(ticker, purchase_date, investment_amount):
    """
    Calculates the current value of an investment based on the historical stock price.

    Parameters:
        ticker (str): The stock ticker symbol.
        purchase_date (str): The date of purchase in 'YYYY-MM-DD' format.
        investment_amount (float): The amount of money initially invested.

    Returns:
        float or str: The current value of the investment, or an error message if no historical data is available.
    """
    initial_price = get_historical_stock_price(ticker, purchase_date)

    if initial_price == None:
        return "Invalid date or ticker"

    current_price = get_current_stock_price(ticker)

    shares_bought = investment_amount / initial_price
    current_value = shares_bought * current_price

    return current_value


def load_portfolio(filename):
    """
    Loads the portfolio from a JSON file.

    Parameters:
        filename (str): The file path of the portfolio JSON.

    Returns:
        dict: The loaded portfolio data.
    """
    with open(filename, 'r') as f:
        portfolio = json.load(f)
    return portfolio


def calculate_total_portfolio_value(portfolio):
    """
    Calculates the total current value of all stocks in the portfolio.

    Parameters:
        portfolio (dict): A dictionary containing the portfolio data.

    Returns:
        float: The total value of the portfolio.
    """
    total_value = 0
    for stock in portfolio['stocks']:
        ticker = stock['ticker']
        purchase_date = stock['date']
        investment_amount = stock['amount_in_dollars']

        current_value = calculate_investment_value(
            ticker, purchase_date, investment_amount)

        if isinstance(current_value, str):
            print(f"Error calculating value for {ticker}: {current_value}")
        else:
            total_value += current_value

    return total_value


# Load the portfolio JSON
portfolio_file = 'portfolio.json'
portfolio_data = load_portfolio(portfolio_file)

# Calculate total portfolio value
total_portfolio_value = calculate_total_portfolio_value(portfolio_data)

print("Total value of the portfolio is: $" + str(total_portfolio_value))
