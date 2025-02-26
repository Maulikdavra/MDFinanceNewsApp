# MDFinance

An AI-powered financial news aggregation and analysis platform built with Streamlit.

## Features

- Real-time stock price tracking
- AI-powered news summarization
- Sentiment analysis for news articles
- Company watchlist management
- Interactive stock price charts

## Technologies Used

- Python 3.x
- Streamlit
- OpenAI GPT-4
- yfinance for stock data
- News API for real-time news

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mdfinance.git
cd mdfinance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEWS_API_KEY`: Your News API key

4. Run the application:
```bash
streamlit run main.py
```

## Project Structure

```
├── main.py              # Main application file
├── utils/              # Utility modules
│   ├── ai_analyzer.py   # AI analysis functions
│   ├── news_fetcher.py  # News API integration
│   └── stock_fetcher.py # Stock data fetching
└── styles/             # CSS styles
    └── custom.css      # Custom styling
```

## Contributing

Feel free to open issues and pull requests for any improvements you'd like to suggest.

## License

MIT License
