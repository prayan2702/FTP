import streamlit as st
import pandas as pd
import zipline.api as zp
from zipline import run_algorithm
from datetime import datetime
import pytz

# Define trading strategy
def initialize(context):
    context.asset = zp.symbol(context.selected_stock)
    context.invested = False

def handle_data(context, data):
    if not context.invested and data.can_trade(context.asset):
        zp.order_target_percent(context.asset, 1.0)
        context.invested = True
    elif context.invested and not data.can_trade(context.asset):
        zp.order_target_percent(context.asset, 0)
        context.invested = False

# Streamlit UI
st.title("Backtest with Zipline")

# Dropdown for selecting stock
stocks = ["AAPL", "GOOGL", "MSFT", "TSLA"]
selected_stock = st.selectbox("Select a stock to backtest:", stocks)

# Run backtest button
if st.button("Run Backtest"):
    start = datetime(2020, 1, 1, tzinfo=pytz.UTC)
    end = datetime(2023, 1, 1, tzinfo=pytz.UTC)
    
    result = run_algorithm(
        start=start,
        end=end,
        initialize=initialize,
        handle_data=handle_data,
        capital_base=10000,
        data_frequency='daily',
        data={'selected_stock': selected_stock}  # Pass selected stock
    )
    
    st.write("Backtest Completed!")
    st.dataframe(result.portfolio_value)
