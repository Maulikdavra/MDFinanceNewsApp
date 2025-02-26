from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from utils.news_fetcher import NewsFetcher
from utils.ai_analyzer import AIAnalyzer
from utils.stock_fetcher import StockFetcher
import os

app = Flask(__name__, static_folder='dist')
CORS(app)  # Enable CORS for all routes

news_fetcher = NewsFetcher()
ai_analyzer = AIAnalyzer()
stock_fetcher = StockFetcher()

@app.route('/api/news/<company>')
def get_news(company):
    try:
        articles = news_fetcher.fetch_news(company)
        for article in articles:
            # Add AI analysis
            article['summary'] = ai_analyzer.summarize_news(article['description'])
            article['sentiment'] = ai_analyzer.analyze_sentiment(article['description'])
        return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<company>')
def get_stock(company):
    try:
        stock_data = stock_fetcher.get_stock_data(company)
        if stock_data:
            return jsonify(stock_data)
        return jsonify({'error': 'Stock data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve React app - this needs to be after API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Always return index.html for any unknown routes (client-side routing)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Kill any existing process on port 5000
    os.system('fuser -k 5000/tcp >/dev/null 2>&1 || true')
    app.run(host='0.0.0.0', port=5000)