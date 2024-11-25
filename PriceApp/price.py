import yfinance as yf
from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt


from JSON_Validation.validator import validate_portfolio, load_schema, load_portfolio


def fetch_portfolio_sharpe_ratio(portfolio, price_data, total_investment, risk_free_rate=0.03):
    '''
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
    '''

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
            # Check if the Date exists in the price data
            if Date not in price_data.index:
                # If not, get the last available close date
                last_valid_date = price_data.index[price_data.index <= Date].max(
                )
                if pd.isnull(last_valid_date):
                    print(
                        f"No available price data for {ticker} before {Date}.")
                    return None
                Date = last_valid_date

            # Get stock price from the last valid date
            stock_price = price_data[ticker].loc[Date]
            total_value += nShares * stock_price

        except KeyError as e:
            print(f"Error fetching price for {ticker} on {Date}: {e}")
            return None

    return total_value


def fetch_price_data(tickers, period="5y"):
    """
    Fetch historical price data for a list of tickers over a specified period.

    Parameters:
        tickers (list): A list of stock ticker symbols.
        period (str): The time period for fetching data (default at 5y).

    Returns:
        DataFrame: Adjusted close prices for each ticker.
    """
    data = yf.download(tickers, period=period, interval="1d")['Close']
    return data


def calculate_portfolio_value_over_time(price_data, portfolio):
    """
    Calculate the portfolio's value over time based on the historical price data.

    Parameters:
        price_data (DataFrame): Historical price data for the portfolio tickers.
        portfolio (list): A list of dictionaries with 'ticker' and 'nShares'.

    Returns:
        Series: Portfolio value over time.
    """
    portfolio_values = pd.Series(0, index=price_data.index)
    for stock in portfolio:
        ticker = stock['ticker']
        nShares = stock['nShares']
        if ticker in price_data.columns:
            portfolio_values += price_data[ticker] * nShares
    return portfolio_values


def calculate_rolling_sharpe_ratio(price_data, portfolio, lookback_window=252, risk_free_rate=0.03):
    """
    Calculate the rolling Sharpe Ratio for the portfolio over time.

    Parameters:
        price_data (DataFrame): Historical price data for each stock in the portfolio.
        portfolio (list): A list of dictionaries with 'ticker' and 'nShares'.
        lookback_window (int): The lookback window for the rolling Sharpe Ratio in trading days (default is 252 days, i.e., 1 year).
        risk_free_rate (float): The annual risk-free rate (default is 3%).

    Returns:
        Series: Rolling Sharpe Ratio for the portfolio.
    """
    try:
        # Calculate portfolio values over time
        portfolio_values = calculate_portfolio_value_over_time(
            price_data, portfolio)

        # calculate daily returns of the portfolio
        daily_returns = portfolio_values.pct_change().dropna()

        # convert annual risk-free rate to daily
        daily_risk_free_rate = risk_free_rate / 252

        # Calculate rolling average daily returns and rolling standard deviation
        rolling_avg_daily_return = daily_returns.rolling(
            lookback_window).mean()
        rolling_stddev_daily_return = daily_returns.rolling(
            lookback_window).std()

        # calculate the rolling Sharpe Ratio
        rolling_sharpe_ratio = (
            rolling_avg_daily_return - daily_risk_free_rate) / rolling_stddev_daily_return

        # sanity check
        # print(rolling_sharpe_ratio.iloc[-1])

        return rolling_sharpe_ratio

    except Exception as e:
        print(f"Error calculating rolling Sharpe Ratio: {e}")
        return None


def display_performance_visualizations(price_data, portfolio_values, portfolio, total_portfolio_value, sharpe_ratio):
    """
    Display individual stock values (price * shares) and total portfolio value over time on a single chart.

    Parameters:
        price_data (DataFrame): Historical price data for each stock in the portfolio.
        portfolio_values (Series): Total portfolio value over time.
        portfolio (list): Portfolio details with ticker and number of shares for each stock.
    """
    plt.figure(figsize=(14, 7))

    # Plot individual stock's value over time
    for stock in portfolio:
        ticker = stock['ticker']
        nShares = stock['nShares']
        if ticker in price_data.columns:
            # Calculate the stock's value in the portfolio
            stock_value = price_data[ticker] * nShares
            # Label each stock by ticker
            plt.plot(stock_value, label=f"{ticker} Value")

    # Plot total portfolio value with a thicker line
    plt.plot(portfolio_values, label="Total Portfolio Value",
             linewidth=2.5, color="black")

    # axis
    plt.title("Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Value (Price * Shares)")
    plt.legend()

    # Sharpe and PV
    plt.text(0.5, -0.15, f"Current Portfolio Value: ${total_portfolio_value:,.2f}    |    Sharpe Ratio: {sharpe_ratio:.2f}",
             ha='center', va='top', transform=plt.gca().transAxes, fontsize=12, color="black")

    plt.tight_layout()
    plt.show()


def display_combined_visualizations(price_data, portfolio_values, portfolio, total_portfolio_value, sharpe_ratio, rolling_sharpe_ratio):
    """
    Display individual stock values, total portfolio value, and rolling Sharpe Ratio side by side.

    Parameters:
        price_data (DataFrame): Historical price data for each stock in the portfolio.
        portfolio_values (Series): Total portfolio value over time.
        portfolio (list): Portfolio details with ticker and number of shares for each stock.
        total_portfolio_value (float): Current total value of the portfolio.
        sharpe_ratio (float): Sharpe Ratio of the portfolio.
        rolling_sharpe_ratio (Series): Rolling Sharpe Ratio for the portfolio.
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # plot stock values and total portfolio value on axis 0
    for stock in portfolio:
        ticker = stock['ticker']
        nShares = stock['nShares']
        if ticker in price_data.columns:
            stock_value = price_data[ticker] * nShares
            axes[0].plot(stock_value, label=f"{ticker} Value")

    axes[0].plot(portfolio_values, label="Total Portfolio Value",
                 linewidth=2.5, color="black")
    axes[0].set_title("Portfolio Value Over Time")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Value (Price * Shares)")
    axes[0].legend()

    # text
    axes[0].text(0.5, -0.15, f"Current Portfolio Value: ${total_portfolio_value:,.2f}    |    Sharpe Ratio: {sharpe_ratio:.2f}",
                 ha='center', va='top', transform=axes[0].transAxes, fontsize=12, color="black")

    # Plot rolling Sharpe Ratio on the second axis
    axes[1].plot(rolling_sharpe_ratio,
                 label="Rolling Sharpe Ratio", color="blue")
    axes[1].axhline(0, color="red", linestyle="--", label="Zero Line")
    axes[1].set_title("Rolling Sharpe Ratio Over Time")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Sharpe Ratio")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def calculate_value_sharpe():
    """
    Function to run calculations against validated portfolio
    """

    validated_portfolio = load_and_validate_portfolio()

    if validated_portfolio:
        # Extract tickers from the validated portfolio
        tickers = [stock['ticker'] for stock in validated_portfolio]

        # Fetch historical price data for the tickers
        price_data = yf.download(tickers, period='1y', progress=False)['Close']

        # Calculate the total value of the portfolio
        total_portfolio_value = calculate_total_portfolio_value(
            validated_portfolio, price_data)
        print("Total value of the portfolio is: $" + str(total_portfolio_value))

        # Calculate the Sharpe ratio
        sharpe_ratio = fetch_portfolio_sharpe_ratio(
            validated_portfolio, price_data, total_portfolio_value)
        if sharpe_ratio is not None:
            print("Sharpe ratio of the portfolio is " + str(sharpe_ratio))
            if visualization:
                price_data = fetch_price_data(tickers, period='5y')
                portfolio_values = calculate_portfolio_value_over_time(
                    price_data, validated_portfolio)

                # Calculate rolling Sharpe Ratio
                rolling_sharpe_ratio = calculate_rolling_sharpe_ratio(
                    price_data, validated_portfolio)

                # Display combined visualizations
                if rolling_sharpe_ratio is not None:
                    display_combined_visualizations(
                        price_data, portfolio_values, validated_portfolio, total_portfolio_value, sharpe_ratio, rolling_sharpe_ratio)

        else:
            print("Could not calculate Sharpe ratio due to missing data.")
    else:
        print("Portfolio validation failed. Cannot calculate total value.")


# Check if the script is being executed directly
if __name__ == "__main__":
    visualization = True
    calculate_value_sharpe()
else:
    visualization = False


# code to generate test_data.json
# test_data = yf.download(tickers, period='1y', progress=False)['Close']
# test_data.to_json('test_data.json')
