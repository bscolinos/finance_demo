import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_returns(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily returns from price data"""
    returns = data['Close'].pct_change()
    return returns.fillna(0)

def calculate_portfolio_metrics(portfolio_data: dict) -> dict:
    """Calculate key portfolio metrics"""
    metrics = {
        'total_value': 0,
        'daily_return': 0,
        'ytd_return': 0,
        'risk_metrics': {}
    }
    
    # Calculate total value and returns
    total_value = sum(position['value'] for position in portfolio_data['holdings'])
    daily_changes = sum(position['daily_change'] for position in portfolio_data['holdings'])
    
    metrics['total_value'] = total_value
    metrics['daily_return'] = (daily_changes / total_value) if total_value > 0 else 0
    
    # Calculate risk metrics
    position_weights = [position['value'] / total_value for position in portfolio_data['holdings']]
    metrics['risk_metrics']['diversification_score'] = 1 - sum(w**2 for w in position_weights)
    
    return metrics

def format_currency(value: float) -> str:
    """Format number as currency"""
    return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.2f}%"
