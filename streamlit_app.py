import streamlit as st
import pandas as pd
from utils.news_fetcher import NewsFetcher
from utils.ai_analyzer import AIAnalyzer
from utils.stock_fetcher import StockFetcher

# Page configuration
st.set_page_config(
    page_title="MDFinance",
    page_icon="📈",
    layout="wide"
)

# Initialize classes
news_fetcher = NewsFetcher()
ai_analyzer = AIAnalyzer()
stock_fetcher = StockFetcher()

# Initialize session state
if 'selected_companies' not in st.session_state:
    st.session_state.selected_companies = []

# Header
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a237e, #0d47a1); color: white; border-radius: 12px; margin-bottom: 2rem;'>
        <h1>📈 MDFinance</h1>
        <p style='opacity: 0.9; font-size: 1.2rem;'>Your AI-Powered Financial News Hub</p>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Add Company")
    with st.form(key='add_company_form'):
        company = st.text_input("Enter a company name")
        submit_button = st.form_submit_button(label="Add Company")
        
        if submit_button and company.strip():
            if len(st.session_state.selected_companies) >= 5:
                st.warning("Maximum 5 companies can be added.")
            elif company not in st.session_state.selected_companies:
                st.session_state.selected_companies.append(company)
                st.success(f"Added {company} to your watchlist!")
                st.rerun()

    if st.button("Clear All Companies"):
        st.session_state.selected_companies = []
        st.session_state.current_company = None
        st.success("Cleared all companies!")
        st.rerun()

    # Display company list
    if st.session_state.selected_companies:
        st.markdown("### Your Companies")
        for company in st.session_state.selected_companies:
            cols = st.columns([4, 1])
            with cols[0]:
                if st.button(company, key=f"select_{company}", use_container_width=True):
                    st.session_state.current_company = company
                    st.rerun()
            with cols[1]:
                if st.button("🗑", key=f"remove_{company}", help=f"Remove {company}"):
                    st.session_state.selected_companies.remove(company)
                    if 'current_company' in st.session_state and st.session_state.current_company == company:
                        st.session_state.current_company = None
                    st.success(f"Removed {company}")
                    st.rerun()

with col2:
    if 'current_company' in st.session_state and st.session_state.current_company:
        company = st.session_state.current_company
        
        # Stock information
        try:
            stock_data = stock_fetcher.get_stock_data(company)
            if stock_data:
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Current Price", f"${stock_data['price']:.2f}", f"{stock_data['change_percent']:.2f}%")
                with cols[1]:
                    st.metric("Change", f"${abs(stock_data['change']):.2f}")
                with cols[2]:
                    st.metric("Volume", f"{stock_data['volume']:,}")
                
                # Stock chart
                if stock_data['history']:
                    st.line_chart(pd.Series(stock_data['history']))
        except Exception as e:
            st.warning(f"Unable to fetch stock data: {str(e)}")

        # News section
        st.markdown(f"### Latest News for {company}")
        
        # News category filter
        category = st.selectbox(
            "Filter by Category",
            ["All", "Technology", "Market", "Press Releases"]
        )

        try:
            with st.spinner(f'Fetching news for {company}...'):
                news_articles = news_fetcher.fetch_news(company)
                
                if category != "All":
                    news_articles = [
                        article for article in news_articles 
                        if ai_analyzer.categorize_news(article['title'])['category'] == category
                    ]

                if not news_articles:
                    st.info(f"No {category.lower() if category != 'All' else ''} news found for {company}")
                else:
                    for article in news_articles:
                        with st.expander(article['title']):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**Source:** {article['source']}")
                                st.markdown(f"**Published:** {article['publishedAt']}")
                                st.markdown("**Summary:**")
                                summary = ai_analyzer.summarize_news(article['description'])
                                st.write(summary)
                                
                            with col2:
                                sentiment = ai_analyzer.analyze_sentiment(article['description'])
                                st.markdown("**Sentiment Analysis:**")
                                st.progress(sentiment['confidence'])
                                st.markdown(f"Rating: {'⭐' * sentiment['rating']}")
                            
                            st.markdown(f"[Read full article]({article['url']})")
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
    else:
        st.info("Select a company from the list to view its news and stock information")
