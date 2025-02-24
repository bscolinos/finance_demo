import yfinance as yf
import pandas as pd
import numpy as np

class StockService:
    @staticmethod
    def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            raise Exception(f"Failed to fetch stock data for {symbol}: {e}")

    @staticmethod
    def get_portfolio_performance(positions: dict) -> dict:
        """Calculate portfolio performance"""
        performance = {
            'total_value': 0,
            'daily_change': 0,
            'holdings': []
        }
        
        for symbol, quantity in positions.items():
            stock = yf.Ticker(symbol)
            current_price = stock.info.get('regularMarketPrice', 0)
            prev_close = stock.info.get('previousClose', 0)
            
            position_value = current_price * quantity
            daily_change = (current_price - prev_close) * quantity
            
            performance['holdings'].append({
                'symbol': symbol,
                'quantity': quantity,
                'value': position_value,
                'daily_change': daily_change
            })
            
            performance['total_value'] += position_value
            performance['daily_change'] += daily_change
            
        return performance

    @staticmethod
    def get_market_summary() -> dict:
        """Get summary of major market indices"""
        indices = ['^GSPC', '^DJI', '^IXIC']  # S&P 500, Dow Jones, NASDAQ
        summary = {}
        
        for index in indices:
            idx = yf.Ticker(index)
            info = idx.info
            summary[index] = {
                'name': info.get('shortName', ''),
                'price': info.get('regularMarketPrice', 0),
                'change': info.get('regularMarketChangePercent', 0)
            }
            
        return summary
