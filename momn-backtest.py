# app.py
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time

# Hard-coded credentials
USERNAME = "prayan"
PASSWORD = "prayan"

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login page function
def login():
    st.title("Login")
    with st.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")
        if submit_button:
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()  # Reload the app after login
            else:
                st.error("Invalid username or password")

# Main app content function
def app_content():
    st.title("Momentum Strategy Backtesting")

    # Sidebar for user inputs
    st.sidebar.header("Backtesting Parameters")
    start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime(2023, 12, 29))
    rebalance_frequency = st.sidebar.selectbox("Rebalancing Frequency", ["Monthly", "Quarterly"])
    universe = st.sidebar.selectbox("Universe", ["Nifty50", "Nifty100", "Nifty200", "Nifty500"])
    ranking_method = st.sidebar.selectbox("Ranking Method", ["avgZScore12_6_3", "avgSharpe12_6_3", "avgSharpe9_6_3"])

    # Run backtest when the user clicks the button
    if st.sidebar.button("Run Backtest"):
        st.write(f"Running backtest from {start_date} to {end_date} with {rebalance_frequency} rebalancing...")

        # Simulate backtesting (replace this with actual backtesting logic)
        with st.spinner("Backtesting in progress..."):
            time.sleep(5)  # Simulate a delay
            st.success("Backtest completed!")

            # Display dummy results
            st.write("### Backtest Results")
            results = pd.DataFrame({
                "Date": pd.date_range(start=start_date, end=end_date, freq="D"),
                "Portfolio Value": np.random.rand(365 * 4) * 1000000  # Random portfolio value
            })
            st.line_chart(results.set_index("Date"))

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    app_content()
