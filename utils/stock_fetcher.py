import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class StockFetcher:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes cache

    def get_stock_data(self, company_name):
        """
        Get stock data for a company using its ticker symbol
        """
        try:
            # Simple mapping for demo (in real app, would use a proper company-to-ticker mapping)
            ticker = company_name.split()[0].upper()
            
            # Check cache
            if ticker in self.cache:
                timestamp, data = self.cache[ticker]
                if datetime.now() - timestamp < timedelta(seconds=self.cache_timeout):
                    return data

            # Fetch stock data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get historical data for the chart
            hist = stock.history(period="1mo")
            
            data = {
                'symbol': ticker,
                'price': info.get('regularMarketPrice', 0),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('regularMarketVolume', 0),
                'market_cap': info.get('marketCap', 0),
                'history': hist['Close'].to_dict() if not hist.empty else {}
            }
            
            # Update cache
            self.cache[ticker] = (datetime.now(), data)
            return data

        except Exception as e:
            print(f"Error fetching stock data: {str(e)}")
            return None
