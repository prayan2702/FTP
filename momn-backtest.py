import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Function to calculate portfolio returns
def calculate_portfolio_returns(portfolio, start_date, end_date):
    portfolio_returns = pd.DataFrame()
    for ticker in portfolio:
        data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        returns = data.pct_change().dropna()
        portfolio_returns[ticker] = returns
    portfolio_returns['Portfolio'] = portfolio_returns.mean(axis=1)
    return portfolio_returns

# Function to display backtesting results
def display_backtesting_results(portfolio_returns):
    st.write("### Portfolio Returns Over Time")
    st.line_chart(portfolio_returns['Portfolio'].cumsum())

    st.write("### Portfolio Statistics")
    st.write(f"**Total Return:** {portfolio_returns['Portfolio'].sum() * 100:.2f}%")
    st.write(f"**Annualized Return:** {portfolio_returns['Portfolio'].mean() * 252 * 100:.2f}%")
    st.write(f"**Annualized Volatility:** {portfolio_returns['Portfolio'].std() * np.sqrt(252) * 100:.2f}%")
    st.write(f"**Sharpe Ratio:** {portfolio_returns['Portfolio'].mean() / portfolio_returns['Portfolio'].std() * np.sqrt(252):.2f}")

# Main function for the Streamlit app
def main():
    st.title("Portfolio Backtesting App")

    # Dropdown to select ranking method
    ranking_methods = ["AvgZScore 12M/6M/3M", "AvgZScore 12M/9M/6M/3M", "AvgSharpe 12M/6M/3M", "AvgSharpe 9M/6M/3M", "AvgSharpe 12M/9M/6M/3M", "Sharpe12M", "Sharpe3M"]
    selected_method = st.selectbox("Select Ranking Method", ranking_methods)

    # Date range selection
    start_date = st.date_input("Start Date", datetime.today() - timedelta(days=365))
    end_date = st.date_input("End Date", datetime.today())

    # Load the ranking data (assuming it's stored in a CSV file)
    ranking_data = pd.read_csv("ranking_results.csv")  # Replace with actual file path

    # Filter the ranking data based on the selected method
    filtered_data = ranking_data[ranking_data['Ranking Method'] == selected_method]

    # Select top N stocks for the portfolio
    top_n = st.slider("Select Top N Stocks", min_value=1, max_value=50, value=10)
    portfolio = filtered_data.head(top_n)['Ticker'].tolist()

    # Run backtesting
    if st.button("Run Backtest"):
        portfolio_returns = calculate_portfolio_returns(portfolio, start_date, end_date)
        display_backtesting_results(portfolio_returns)

if __name__ == "__main__":
    main()
