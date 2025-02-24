import streamlit as st
from services.news_service import NewsService
from services.ai_service import AIService

def display_news_dashboard():
    """Display news dashboard"""
    news_service = NewsService()
    ai_service = AIService()
    
    # Search bar
    search_query = st.text_input("Search News", placeholder="Enter keywords or stock symbols")
    
    if search_query:
        news_articles = news_service.search_news(search_query)
    else:
        news_articles = news_service.get_market_news()
    
    # Display sentiment analysis if articles are found
    if news_articles:
        sentiment = ai_service.get_market_sentiment(news_articles)
        
        # Display sentiment metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Market Sentiment", sentiment['overall_sentiment'])
        with col2:
            st.metric("Confidence", f"{sentiment['confidence']*100:.1f}%")
        
        st.write("Key Factors:")
        for factor in sentiment['key_factors']:
            st.write(f"• {factor}")
        
        st.write("Market Outlook:", sentiment['market_outlook'])
    
    # Display news articles
    st.subheader("Latest News")
    for article in news_articles:
        with st.expander(article['title']):
            st.write(f"**Source:** {article['source']['name']}")
            st.write(f"**Published:** {article['publishedAt']}")
            st.write(article['description'])
            st.markdown(f"[Read more]({article['url']})")
