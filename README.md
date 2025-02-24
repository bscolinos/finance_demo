# AI Financial Advisor

A Streamlit-based financial advisor application that provides intelligent portfolio management, real-time stock insights, and news tracking capabilities.

## Project Structure

```
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── components/
│   ├── charts.py        # Data visualization components
│   ├── news.py          # News display components
│   └── portfolio.py     # Portfolio management components
├── services/
│   ├── ai_service.py    # OpenAI integration
│   ├── news_service.py  # NewsAPI integration
│   └── stock_service.py # yfinance integration
├── utils/
│   └── data_utils.py    # Data processing utilities
└── main.py              # Main application entry point
```

## Setup Instructions

1. Install dependencies:
```bash
pip install streamlit yfinance newsapi-python plotly openai
```

2. Set up API keys:
- Create a `.env` file and add your API keys:
```
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key
```

3. Run the application:
```bash
streamlit run main.py
```

## Database Integration Points

For database integration, consider:

1. Create a new `database/` directory with:
   - `models.py` for database models
   - `database.py` for database connection
   - `repository.py` for database operations

2. Key tables needed:
   - Users
   - Portfolios
   - Positions
   - Transactions
   - WatchLists

3. Update these files to use database:
   - `components/portfolio.py`: Replace sample data with database queries
   - `services/stock_service.py`: Add position tracking
   - `main.py`: Add user authentication

## Current Features

1. Portfolio Dashboard
   - Portfolio overview with key metrics
   - Holdings table
   - Performance charts
   - Quick actions

2. News Tracker
   - Financial news search
   - Market news feed
   - Stock-specific news

3. AI Insights
   - Portfolio analysis
   - Market sentiment analysis

## Dependencies

- Python 3.11
- Streamlit
- yfinance
- NewsAPI
- Plotly
- OpenAI

## Future Features

- Real-time stock price updates
- Advanced AI-powered financial insights
- Portfolio optimization suggestions
