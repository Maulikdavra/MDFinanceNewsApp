import os
from newsapi import NewsApiClient
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))
    
    def fetch_news(self, company_name):
        """
        Fetch news articles for a specific company
        """
        try:
            # Get news from the last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')
            
            articles = self.newsapi.get_everything(
                q=company_name,
                from_param=from_date,
                to=to_date,
                language='en',
                sort_by='relevancy',
                page_size=10
            )
            
            # Format articles
            formatted_articles = []
            for article in articles['articles']:
                formatted_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'publishedAt': datetime.strptime(
                        article.get('publishedAt', ''), 
                        '%Y-%m-%dT%H:%M:%SZ'
                    ).strftime('%Y-%m-%d %H:%M')
                })
            
            return formatted_articles
            
        except Exception as e:
            raise Exception(f"Failed to fetch news: {str(e)}")
