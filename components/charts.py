import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from services.stock_service import StockService
import pandas as pd

def plot_portfolio_performance():
    """Display portfolio performance charts"""
    # Sample portfolio data (in real app, this would come from a database)
    portfolio = {
        'AAPL': 10,
        'GOOGL': 5,
        'MSFT': 8
    }
    
    # Get historical data for each stock
    historical_data = {}
    for symbol in portfolio:
        data = StockService.get_stock_data(symbol)
        historical_data[symbol] = data
    
    # Create performance chart
    fig = go.Figure()
    
    for symbol, data in historical_data.items():
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                name=symbol,
                mode='lines'
            )
        )
    
    fig.update_layout(
        title='Portfolio Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create allocation pie chart
    performance = StockService.get_portfolio_performance(portfolio)
    holdings_df = pd.DataFrame(performance['holdings'])
    
    fig_pie = px.pie(
        holdings_df,
        values='value',
        names='symbol',
        title='Portfolio Allocation'
    )
    
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False)
    
    st.plotly_chart(fig_pie, use_container_width=True)
