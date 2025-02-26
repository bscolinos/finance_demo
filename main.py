import streamlit as st
import os
import singlestoredb as s2
from components import portfolio, news, charts
from services.stock_service import StockService
from services.news_service import NewsService
from services.ai_service import AIService
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import multiprocessing
from streamlit_autorefresh import st_autorefresh

load_dotenv()

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import database initialization and repository for live_trades table
from database.database import init_db
from database.repository import TradeRepository

# Import the trade simulator module (runs the simulation process)
import tradeSimulator.simulator as simulator


def insert_optimized_portfolio(optimized_portfolio_data: dict, user_id: str):
    """
    Inserts optimized portfolio positions into SingleStore.
    """
    config = {
        "host": os.getenv('host'),
        "port": os.getenv('port'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "database": os.getenv('database')
    }
    connection = s2.connect(**config)
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS optimized_portfolio (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(100),
        symbol VARCHAR(10),
        quantity INT,
        target_allocation FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Clear previous optimizations for this user
    cursor.execute("DELETE FROM optimized_portfolio WHERE user_id = %s", (user_id, ))

    insert_query = '''
    INSERT INTO optimized_portfolio (user_id, symbol, quantity, target_allocation)
    VALUES (%s, %s, %s, %s);
    '''

    for holding in optimized_portfolio_data.get("optimized_holdings", []):
        data_tuple = (user_id, holding["symbol"], holding["quantity"], holding["target_allocation"])
        cursor.execute(insert_query, data_tuple)

    connection.commit()
    cursor.close()
    connection.close()


def main():
    st.title("AI Financial Advisor 📈")

    # Initialize the live_trades table using your database module
    init_db()

    # Start the trade simulator process in the background (runs only once per session)
    if "simulation_started" not in st.session_state:
        sim_process = multiprocessing.Process(target=simulator.main, daemon=True)
        sim_process.start()
        st.session_state.simulation_started = True
        st.sidebar.info("Trade simulator started in background.")

    # Sidebar navigation with an added Real-Time Trading View option
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page",
        ["Welcome", "Portfolio Dashboard", "News Tracker", "AI Insights", "Real-Time Trading View"]
    )

    # Initialize session state for user_id if not already set
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ''

    if page == "Welcome":
        st.header("Welcome to AI Financial Advisor")

        # User identification
        if not st.session_state.user_id:
            user_id = st.text_input("Enter your name:", key="user_name_input")
            if user_id:
                st.session_state.user_id = user_id
                st.success(f"Welcome, {user_id}!")
        else:
            st.write(f"Welcome back, {st.session_state.user_id}!")

        user_goals = st.text_input("Enter your investment goals here:")
        if user_goals:
            st.write("Optimizing your portfolio based on your goals...")
            # Sample portfolio data used for optimization; in a real app this would come from user data
            sample_portfolio = {
                'holdings': [{
                    'symbol': 'AAPL',
                    'quantity': 10,
                    'value': 1750.00
                }, {
                    'symbol': 'GOOGL',
                    'quantity': 5,
                    'value': 3250.00
                }, {
                    'symbol': 'MSFT',
                    'quantity': 8,
                    'value': 2800.00
                }],
                'total_value': 7800.00,
                'daily_change': 120.50
            }
            # Get optimized portfolio from the LLM based on the user's goals
            ai_service = AIService()
            optimized_portfolio = ai_service.optimize_portfolio(sample_portfolio, user_goals)
            st.subheader("Optimized Portfolio")
            st.json(optimized_portfolio)

            # Insert the optimized positions into SingleStore with user_id
            insert_optimized_portfolio(optimized_portfolio, st.session_state.user_id)
            st.success("Optimized portfolio positions have been saved into the database!")

    elif page == "Portfolio Dashboard":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Portfolio Overview")
            portfolio.display_portfolio_summary()
            st.subheader("Performance Charts")
            charts.plot_portfolio_performance()
        with col2:
            st.subheader("Quick Actions")
            portfolio.display_quick_actions()
            st.subheader("Market Summary")
            portfolio.display_market_summary()

    elif page == "News Tracker":
        news.display_news_dashboard()

    elif page == "AI Insights":
        st.subheader("AI-Powered Insights")
        sample_portfolio = {
            'holdings': [{
                'symbol': 'AAPL',
                'quantity': 10,
                'value': 1750.00
            }, {
                'symbol': 'GOOGL',
                'quantity': 5,
                'value': 3250.00
            }, {
                'symbol': 'MSFT',
                'quantity': 8,
                'value': 2800.00
            }],
            'total_value': 7800.00,
            'daily_change': 120.50
        }
        ai_service = AIService()
        portfolio_analysis = ai_service.get_portfolio_insights(sample_portfolio)
        st.write(portfolio_analysis)

        news_service = NewsService()
        market_news = news_service.get_market_news(limit=5)
        sentiment = ai_service.get_market_sentiment(market_news)
        st.subheader("Market Sentiment Analysis")
        st.write(sentiment)

    elif page == "Real-Time Trading View":
        st.header("Real-Time Trading View")
        st.write("Live trades and price chart updated every 500 ms.")

        # Auto-refresh the page every 500 ms using streamlit-autorefresh
        st_autorefresh(interval=500, key="trades_autorefresh")

        # Query the latest trades using your TradeRepository
        repo = TradeRepository()
        try:
            trades_df = repo.get_latest_trades(limit=50)
        except Exception as e:
            st.error(f"Error retrieving trades: {e}")
            trades_df = None

        if trades_df is not None and not trades_df.empty:
            # Debug: display the first few rows of the raw data
            st.write("Raw trade data (first 5 rows):", trades_df.head())

            # Convert the nanosecond timestamp to a datetime for proper plotting
            try:
                trades_df['datetime'] = pd.to_datetime(
                    trades_df['participant_timestamp'], unit='ns', errors='coerce'
                )
            except Exception as e:
                st.error(f"Error converting timestamps: {e}")

            # Ensure the 'price' column is numeric (in case it comes as a string)
            trades_df['price'] = pd.to_numeric(trades_df['price'], errors='coerce')

            st.subheader("Latest Trades")
            st.dataframe(trades_df.sort_values("participant_timestamp", ascending=False))

            st.subheader("Price Over Time")
            fig = px.line(
                trades_df.sort_values("datetime"),
                x="datetime",
                y="price",
                title="Trade Price Trend"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trade data available yet.")


if __name__ == "__main__":
    main()
