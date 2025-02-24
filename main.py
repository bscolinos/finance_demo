import streamlit as st
import os
import singlestoredb as s2
from components import portfolio, news, charts
from services.stock_service import StockService
from services.news_service import NewsService
from services.ai_service import AIService
from env import host, port, user, password, database

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def insert_optimized_portfolio(optimized_portfolio_data: dict):
    """
    Inserts optimized portfolio positions into SingleStore.
    Assumes the table 'optimized_portfolio' is already created.
    """
    config = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database
    }
    connection = s2.connect(**config)
    cursor = connection.cursor()
    
    insert_query = '''
    INSERT INTO optimized_portfolio (symbol, quantity, target_allocation)
    VALUES (%s, %s, %s);
    '''
    
    for holding in optimized_portfolio_data.get("optimized_holdings", []):
        data_tuple = (
            holding["symbol"],
            holding["quantity"],
            holding["target_allocation"]
        )
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
        ["Welcome", "Portfolio Dashboard", "News Tracker", "AI Insights"]
    )

    if page == "Welcome":
        st.header("Welcome to AI Financial Advisor")
        user_goals = st.text_input("Enter your investment goals here:")
        if user_goals:
            st.write("Optimizing your portfolio based on your goals...")
            # Sample portfolio data used for optimization; in a real app this would come from user data
            sample_portfolio = {
                'holdings': [
                    {'symbol': 'AAPL', 'quantity': 10, 'value': 1750.00},
                    {'symbol': 'GOOGL', 'quantity': 5, 'value': 3250.00},
                    {'symbol': 'MSFT', 'quantity': 8, 'value': 2800.00}
                ],
                'total_value': 7800.00,
                'daily_change': 120.50
            }
            # Get optimized portfolio from the LLM based on the user's goals
            optimized_portfolio = ai_service.optimize_portfolio(sample_portfolio, user_goals)
            st.subheader("Optimized Portfolio")
            st.json(optimized_portfolio)
            
            # Insert the optimized positions into SingleStore
            insert_optimized_portfolio(optimized_portfolio)
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

    else:  # AI Insights
        st.subheader("AI-Powered Insights")
        sample_portfolio = {
            'holdings': [
                {'symbol': 'AAPL', 'quantity': 10, 'value': 1750.00},
                {'symbol': 'GOOGL', 'quantity': 5, 'value': 3250.00},
                {'symbol': 'MSFT', 'quantity': 8, 'value': 2800.00}
            ],
            'total_value': 7800.00,
            'daily_change': 120.50
        }
        portfolio_analysis = ai_service.get_portfolio_insights(sample_portfolio)
        st.write(portfolio_analysis)

        news_service = NewsService()
        market_news = news_service.get_market_news(limit=5)
        sentiment = ai_service.get_market_sentiment(market_news)
        st.subheader("Market Sentiment Analysis")
        st.write(sentiment)

if __name__ == "__main__":
    main()