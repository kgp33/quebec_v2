import yfinance as yf
from datetime import datetime
import json
import pandas as pd

from JSON_Validation.validator import validate_portfolio, load_schema, load_portfolio

def fetch_portfolio_sharpe_ratio(portfolio, price_data, total_investment, risk_free_rate=0.03):
    """
    Fetches the Sharpe Ratio for the entire portfolio based on historical prices.

    Parameters:
        portfolio: A list of stock dictionaries with 'ticker' and 'nShares'.
        price_data (DataFrame): Price data for a list of tickers.
            Example:
            Ticker                           AAPL        AMZN       GOOGL        MSFT        NVDA        TSLA
            Date                                                                                             
            2023-11-06 00:00:00+00:00  179.229996  139.740005  130.250000  356.529999   45.750999  219.270004
            2023-11-07 00:00:00+00:00  181.820007  142.710007  130.970001  360.529999   45.955002  222.179993
            2023-11-08 00:00:00+00:00  182.889999  142.080002  131.839996  363.200012   46.574001  222.110001
            2023-11-09 00:00:00+00:00  182.410004  140.600006  130.240005  360.690002   46.950001  209.979996
            2023-11-10 00:00:00+00:00  186.399994  143.559998  132.589996  369.670013   48.334999  214.649994
            ...                               ...         ...         ...         ...         ...         ...
            2024-10-29 00:00:00+00:00  233.669998  190.830002  169.679993  431.950012  141.250000  259.519989
            2024-10-30 00:00:00+00:00  230.100006  192.729996  174.460007  432.529999  139.339996  257.549988
            2024-10-31 00:00:00+00:00  225.910004  186.399994  171.110001  406.350006  132.759995  249.850006
            2024-11-01 00:00:00+00:00  222.910004  197.929993  171.289993  410.369995  135.399994  248.979996
            2024-11-04 00:00:00+00:00  220.820007  194.955002  168.449997  406.850006  137.583298  244.539993
            * get price for 'AAPL' on '2024-10-30' : price_data['AAPL].loc['2024-10-30']
        risk_free_rate (float): The risk-free rate for calculating the Sharpe Ratio (default is 3% annually).

    Returns:
        float: The Sharpe Ratio for the entire portfolio.
    """
    try:
        # Create an empty DataFrame to hold daily portfolio returns
        portfolio_daily_returns = pd.DataFrame()

        # Loop through each stock in the portfolio
        for stock in portfolio:
            ticker = stock['ticker']
            nShares = stock['nShares']

            # Calculate weight using today's price
            try:
                current_price = price_data[ticker].iloc[-1]
                # Weight of the stock in the portfolio
                weight = (current_price * nShares) / total_investment
            except Exception as e:
                print(f"Error fetching current price for {ticker}: {e}")
                continue

            # Check if data is available
            if not price_data[ticker].empty:
                # Get the closing prices and calculate daily returns
                closing_prices = price_data[ticker]
                daily_returns = closing_prices.pct_change().dropna()

                # Add the weighted daily returns of the stock to the portfolio's daily returns
                portfolio_daily_returns[ticker] = daily_returns * weight
            else:
                print(f"No historical data available for {ticker}")
                continue

        # Sum the weighted returns to get the total portfolio daily returns
        portfolio_daily_returns['Portfolio'] = portfolio_daily_returns.sum(
            axis=1)

        # Calculate the average daily return and standard deviation of portfolio returns
        average_daily_return = portfolio_daily_returns['Portfolio'].mean()
        stddev_daily_return = portfolio_daily_returns['Portfolio'].std()

        # Assuming a risk-free rate of 3% per year (converted to daily rate)
        daily_risk_free_rate = risk_free_rate / 252  # 252 trading days in a year

        # Calculate the Sharpe Ratio for the portfolio
        sharpe_ratio = (average_daily_return -
                        daily_risk_free_rate) / stddev_daily_return

        return sharpe_ratio

    except Exception as e:
        print(f"Error fetching historical prices for portfolio: {e}")
        return None

def calculate_total_portfolio_value(portfolio, price_data, Date=datetime.today().strftime('%Y-%m-%d')):
    """
    Calculates the total current value of all stocks in the portfolio on the specific day.

    Parameters:
        portfolio (dict): A dictionary containing the portfolio data.
        price_data (DataFrame): Price data for a list of tickers.
        Date (str): A date in 'YYYY-MM-DD' format. 

    Returns:
        float: The total value of the portfolio.
    """
    total_value = 0
    for stock in portfolio:
        ticker = stock['ticker']
        nShares = stock['nShares']
        try:
            stock_price = price_data[ticker].loc[Date]
            total_value += nShares * stock_price
        except KeyError as e:
            print(f"Error fetching current price for {ticker}: {e}")
            return None
    return total_value


def load_and_validate_portfolio():
    """
    Loads stock.json and validates schema
    Returns validated portfolio
    """
    schema = load_schema('stock-schema.json')
    portfolio = load_portfolio('stock.json')
    validated_portfolio = validate_portfolio(portfolio, schema)
    if validated_portfolio:
        print("Validation passed, ready to proceed.")
        return validated_portfolio
    else:
        print("Validation Failed. Unable to perform calculations.")
        return None

# Load, validate, and calculate total portfolio value
validated_portfolio = load_and_validate_portfolio()['stocks']
portfolio_data = validated_portfolio

if validated_portfolio:
    # Extract tickers from the validated portfolio
    tickers = [stock['ticker'] for stock in validated_portfolio]
    
    # Fetch historical price data for the tickers
    price_data = yf.download(tickers, period='1y', progress=False)['Close']

    # Calculate the total value of the portfolio
    total_portfolio_value = calculate_total_portfolio_value(validated_portfolio, price_data)
    print("Total value of the portfolio is: $" + str(total_portfolio_value))
    
    # Calculate the Sharpe ratio
    sharpe_ratio = fetch_portfolio_sharpe_ratio(validated_portfolio, price_data, total_portfolio_value)
    if sharpe_ratio is not None:
        print("Sharpe ratio of the portfolio is " + str(sharpe_ratio))
    else:
        print("Could not calculate Sharpe ratio due to missing data.")
else:
    print("Portfolio validation failed. Cannot calculate total value.")



# code to generate test_data.json
# test_data = yf.download(tickers, period='1y', progress=False)['Close']
# test_data.to_json('test_data.json')

#code to read in unit test data
#test_data = pd.read_json('test_data.json')

# Calculate the unit test data total portfolio value on today
#total_test_portfolio_value = calculate_total_portfolio_value(
#    portfolio_data, test_data, '2024-11-04')
#print("Total value of the test portfolio today is: " + str(total_test_portfolio_value))

