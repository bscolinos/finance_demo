import os
from anthropic import Anthropic
import json
from dotenv import load_dotenv

load_dotenv()

anthropic_api_key = os.getenv('anthropic_api_key')


class AIService:

    def __init__(self):
        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        self.client = Anthropic(api_key=anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def get_portfolio_insights(self, portfolio_data: dict) -> dict:
        """Generate AI insights for portfolio"""
        try:
            prompt = f"""You are a financial advisor. Analyze this portfolio data and provide insights:
{json.dumps(portfolio_data, indent=2)}

Return your analysis as a JSON object with exactly these keys:
- summary: A string with overall portfolio assessment
- risks: An array of strings listing potential risks
- opportunities: An array of strings listing potential opportunities
- recommendations: An array of strings with actionable recommendations

Format your response as valid JSON only, no other text."""
            response = self.client.messages.create(model=self.model,
                                                   messages=[{
                                                       "role": "user",
                                                       "content": prompt
                                                   }],
                                                   max_tokens=1000)
            return json.loads(response.content[0].text)
        except Exception as e:
            raise Exception(f"Failed to generate portfolio insights: {e}")

    def get_market_sentiment(self, news_articles: list) -> dict:
        """Analyze market sentiment from news"""
        try:
            prompt = f"""You are a financial analyst. Analyze these news articles and provide market sentiment:
{json.dumps(news_articles, indent=2)}

Return your analysis as a JSON object with exactly these keys:
- overall_sentiment: A string that must be either "bullish", "bearish", or "neutral"
- confidence: A float between 0.0 and 1.0
- key_factors: An array of strings listing key market factors
- market_outlook: A string with a brief market outlook

Format your response as valid JSON only, no other text."""
            response = self.client.messages.create(model=self.model,
                                                   messages=[{
                                                       "role": "user",
                                                       "content": prompt
                                                   }],
                                                   max_tokens=1000)
            return json.loads(response.content[0].text)
        except Exception as e:
            raise Exception(f"Failed to analyze market sentiment: {e}")

    def optimize_portfolio(self, portfolio_data: dict,
                           user_goals: str) -> dict:
        """Optimize portfolio according to user stated investment goals."""
        try:
            prompt = f"""You are a financial advisor and portfolio optimizer. Given the following portfolio data and the user's investment goals, optimize the portfolio to best meet the goals.
Portfolio data:
{json.dumps(portfolio_data, indent=2)}

User Goals:
{user_goals}

Return your optimized portfolio as a JSON object with exactly these keys:
- optimized_holdings: an array of objects with keys 'symbol', 'quantity', and 'target_allocation'
- rationale: a string explaining the changes

Format your response as valid JSON only, no additional text."""
            response = self.client.messages.create(model=self.model,
                                                   messages=[{
                                                       "role": "user",
                                                       "content": prompt
                                                   }],
                                                   max_tokens=1000)
            return json.loads(response.content[0].text)
        except Exception as e:
            raise Exception(f"Failed to optimize portfolio: {e}")
