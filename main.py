import streamlit as st
import os
import singlestoredb as s2
from components import portfolio, news, charts
from services.stock_service import StockService
from services.news_service import NewsService
from services.ai_service import AIService

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Financial Advisor",
                   page_icon="📈",
                   layout="wide",
                   initial_sidebar_state="expanded")


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
    cursor.execute("DELETE FROM optimized_portfolio WHERE user_id = %s",
                   (user_id, ))

    insert_query = '''
    INSERT INTO optimized_portfolio (user_id, symbol, quantity, target_allocation)
    VALUES (%s, %s, %s, %s);
    '''

    for holding in optimized_portfolio_data.get("optimized_holdings", []):
        data_tuple = (user_id, holding["symbol"], holding["quantity"],
                      holding["target_allocation"])
        cursor.execute(insert_query, data_tuple)

    connection.commit()
    cursor.close()
    connection.close()


def main():
    st.title("AI Financial Advisor 📈")

    # Initialize services
    stock_service = StockService()
    ai_service = AIService()

    # Sidebar navigation with the new Welcome page
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page",
        ["Welcome", "Portfolio Dashboard", "News Tracker", "AI Insights"])

    # Initialize session state for user_id
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
                'total_value':
                7800.00,
                'daily_change':
                120.50
            }
            # Get optimized portfolio from the LLM based on the user's goals
            optimized_portfolio = ai_service.optimize_portfolio(
                sample_portfolio, user_goals)
            st.subheader("Optimized Portfolio")
            st.json(optimized_portfolio)

            # Insert the optimized positions into SingleStore with user_id
            insert_optimized_portfolio(optimized_portfolio,
                                       st.session_state.user_id)
            st.success(
                "Optimized portfolio positions have been saved into the database!"
            )

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

    else:  # AI Insights
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
            'total_value':
            7800.00,
            'daily_change':
            120.50
        }
        portfolio_analysis = ai_service.get_portfolio_insights(
            sample_portfolio)
        st.write(portfolio_analysis)

        news_service = NewsService()
        market_news = news_service.get_market_news(limit=5)
        sentiment = ai_service.get_market_sentiment(market_news)
        st.subheader("Market Sentiment Analysis")
        st.write(sentiment)


if __name__ == "__main__":
    main()
