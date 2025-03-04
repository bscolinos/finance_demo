import streamlit as st
import pandas as pd
import os
import singlestoredb as s2
from services.stock_service import StockService
from utils.data_utils import format_currency, format_percentage, calculate_portfolio_metrics


def get_optimized_positions():
    """Fetch optimized portfolio positions from SingleStore."""
    config = {
        "host": os.getenv('host'),
        "port": os.getenv('port'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "database": os.getenv('database')
    }
    connection = s2.connect(**config)
    cursor = connection.cursor()

    # Get user_id from session state
    user_id = st.session_state.get('user_id', '')
    
    if not user_id:
        cursor.close()
        connection.close()
        return {}

    query = "SELECT symbol, quantity FROM optimized_portfolio WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    positions = {}
    for row in results:
        # Assuming each row is a tuple (symbol, quantity)
        symbol = row[0]
        quantity = row[1]
        # If multiple rows for the same symbol exist, sum them
        positions[symbol] = positions.get(symbol, 0) + quantity
    return positions


def display_portfolio_summary():
    """Display portfolio summary section using optimized portfolio positions."""
    try:
        positions = get_optimized_positions()
    except Exception as e:
        st.error(f"Error fetching optimized positions: {e}")
        positions = {}

    # If no optimized positions, fallback to sample data.
    if not positions:
        positions = {'AAPL': 10, 'GOOGL': 5, 'MSFT': 8}

    # Get performance metrics based on positions
    performance = StockService.get_portfolio_performance(positions)
    metrics = calculate_portfolio_metrics(performance)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Value", format_currency(metrics['total_value']),
                  format_percentage(metrics['daily_return']))
    with col2:
        st.metric("YTD Return", format_percentage(metrics['ytd_return']))
    with col3:
        st.metric(
            "Diversification Score",
            format_percentage(
                metrics['risk_metrics']['diversification_score'] * 100))

    # Display holdings table
    st.subheader("Holdings")
    holdings_df = pd.DataFrame(performance['holdings'])
    st.dataframe(
        holdings_df.style.format({
            'value': lambda x: format_currency(x),
            'daily_change': lambda x: format_currency(x)
        }))


def display_quick_actions():
    """Display quick actions section."""
    from services.tracking_service import TrackingService
    
    symbol = st.text_input("Add Stock Symbol", placeholder="e.g., AAPL")
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("Quantity", min_value=1, value=1)
    with col2:
        if st.button("Add to Portfolio"):
            TrackingService.log_activity("add_stock", {"symbol": symbol, "quantity": quantity})
    
    if st.button("Rebalance Portfolio"):
        TrackingService.log_activity("rebalance_portfolio")


def display_market_summary():
    """Display market summary section."""
    market_data = StockService.get_market_summary()
    for index, data in market_data.items():
        st.metric(data['name'], format_currency(data['price']),
                  format_percentage(data['change']))
