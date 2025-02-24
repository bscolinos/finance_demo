from newsapi import NewsApiClient
from env import news_api_key

class NewsService:
    def __init__(self):
        api_key = news_api_key
        if not api_key:
            raise Exception("NEWS_API_KEY environment variable is not set")
        self.api = NewsApiClient(api_key=api_key)

    def get_market_news(self, limit: int = 10) -> list:
        """Get general market news"""
        try:
            news = self.api.get_top_headlines(
                category='business',
                language='en',
                country='us',
                page_size=limit
            )

            if news.get('status') == 'error':
                raise Exception(news.get('message', 'Unknown error occurred'))

            return news.get('articles', [])
        except Exception as e:
            raise Exception(f"Failed to fetch market news: {e}")

    def get_stock_news(self, symbol: str, limit: int = 5) -> list:
        """Get news articles for a specific stock"""
        try:
            news = self.api.get_everything(
                q=symbol,
                language='en',
                sort_by='publishedAt',
                page_size=limit
            )

            if news.get('status') == 'error':
                raise Exception(news.get('message', 'Unknown error occurred'))

            return news.get('articles', [])
        except Exception as e:
            raise Exception(f"Failed to fetch news for {symbol}: {e}")

    def search_news(self, query: str, limit: int = 10) -> list:
        """Search news articles by query"""
        try:
            news = self.api.get_everything(
                q=query,
                language='en',
                sort_by='relevancy',
                page_size=limit
            )

            if news.get('status') == 'error':
                raise Exception(news.get('message', 'Unknown error occurred'))

            return news.get('articles', [])
        except Exception as e:
            raise Exception(f"Failed to search news: {e}")