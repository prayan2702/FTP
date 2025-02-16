import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Function to calculate portfolio returns
def calculate_portfolio_returns(portfolio, start_date, end_date):
    """
    Calculate the returns of a portfolio over a given period.
    """
    portfolio_returns = pd.Series(index=pd.date_range(start=start_date, end=end_date), dtype=float)
    for ticker in portfolio:
        try:
            stock_data = yf.download(ticker + ".NS", start=start_date, end=end_date)['Adj Close']
            stock_returns = stock_data.pct_change().fillna(0)
            portfolio_returns += stock_returns * (1 / len(portfolio))  # Equal-weighted portfolio
        except Exception as e:
            st.warning(f"Failed to download data for {ticker}: {e}")
    return portfolio_returns

# Function to backtest the momentum strategy
def backtest_momentum_strategy(start_date, end_date, rebalance_frequency, universe, ranking_method):
    """
    Backtest the momentum ranking strategy over a given period.
    """
    # Initialize variables
    portfolio_returns = pd.Series(dtype=float)
    current_date = start_date

    while current_date <= end_date:
        # Get the top-ranked stocks for the current rebalance date
        try:
            # Simulate the momentum ranking logic (replace this with your actual ranking logic)
            top_stocks = get_top_ranked_stocks(current_date, universe, ranking_method)
            
            # Calculate portfolio returns for the rebalance period
            next_rebalance_date = current_date + pd.DateOffset(months=1) if rebalance_frequency == 'Monthly' else current_date + pd.DateOffset(months=3)
            if next_rebalance_date > end_date:
                next_rebalance_date = end_date
            
            # Calculate returns for the current portfolio
            period_returns = calculate_portfolio_returns(top_stocks, current_date, next_rebalance_date)
            portfolio_returns = pd.concat([portfolio_returns, period_returns])

            # Move to the next rebalance date
            current_date = next_rebalance_date
        except Exception as e:
            st.error(f"Error during backtesting at {current_date}: {e}")
            current_date += pd.DateOffset(months=1)  # Skip to the next month if an error occurs

    return portfolio_returns

# Function to get top-ranked stocks (replace this with your actual ranking logic)
def get_top_ranked_stocks(date, universe, ranking_method):
    """
    Simulate the momentum ranking logic to get the top-ranked stocks.
    Replace this with your actual ranking logic.
    """
    # Example: Return a fixed list of top-ranked stocks (for demonstration purposes)
    if universe == 'AllNSE':
        return ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS']
    else:
        return ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

# Streamlit App
def main():
    st.title("Momentum Strategy Backtesting")
    st.write("This app backtests a momentum-based stock selection strategy.")

    # Sidebar for user inputs
    st.sidebar.header("Backtesting Parameters")
    start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime(2023, 12, 31))
    rebalance_frequency = st.sidebar.selectbox("Rebalancing Frequency", ["Monthly", "Quarterly"])
    universe = st.sidebar.selectbox("Universe", ["AllNSE", "Nifty50", "Nifty100"])
    ranking_method = st.sidebar.selectbox("Ranking Method", ["avgZScore12_6_3", "avgSharpe12_6_3", "avgSharpe9_6_3"])

    # Run backtest when the user clicks the button
    if st.sidebar.button("Run Backtest"):
        st.write(f"Running backtest from {start_date} to {end_date} with {rebalance_frequency} rebalancing...")

        # Backtest the momentum strategy
        strategy_returns = backtest_momentum_strategy(start_date, end_date, rebalance_frequency, universe, ranking_method)

        # Download benchmark data (e.g., Nifty 50)
        benchmark_data = yf.download("^NSEI", start=start_date, end=end_date)['Adj Close']
        benchmark_returns = benchmark_data.pct_change().fillna(0)

        # Calculate cumulative returns
        strategy_cumulative_returns = (1 + strategy_returns).cumprod()
        benchmark_cumulative_returns = (1 + benchmark_returns).cumprod()

        # Plot the results
        st.write("### Cumulative Returns: Momentum Strategy vs Nifty 50")
        plt.figure(figsize=(10, 6))
        plt.plot(strategy_cumulative_returns, label='Momentum Strategy')
        plt.plot(benchmark_cumulative_returns, label='Nifty 50')
        plt.title('Momentum Strategy vs Nifty 50')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.grid()
        st.pyplot(plt)

        # Print performance metrics
        st.write("### Performance Metrics")
        st.write(f"**Strategy Annualized Return:** {(strategy_cumulative_returns[-1] ** (252 / len(strategy_cumulative_returns)) - 1) * 100:.2f}%")
        st.write(f"**Benchmark Annualized Return:** {(benchmark_cumulative_returns[-1] ** (252 / len(benchmark_cumulative_returns)) - 1) * 100:.2f}%")

# Run the Streamlit app
if __name__ == "__main__":
    main()
