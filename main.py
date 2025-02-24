import streamlit as st
import pandas as pd
from utils.news_fetcher import NewsFetcher
from utils.ai_analyzer import AIAnalyzer

# Page configuration
st.set_page_config(
    page_title="AI News Aggregator",
    page_icon="📰",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
if 'selected_companies' not in st.session_state:
    st.session_state.selected_companies = []

def init_classes():
    return NewsFetcher(), AIAnalyzer()

news_fetcher, ai_analyzer = init_classes()

# Header
st.title("📰 AI-Powered News Aggregator")
st.markdown("### Stay informed about your favorite companies")

# Company selection
col1, col2 = st.columns([2, 1])

with col1:
    company = st.text_input("Enter a company name", key="company_input")
    if st.button("Add Company") and company and len(st.session_state.selected_companies) < 5:
        if company not in st.session_state.selected_companies:
            st.session_state.selected_companies.append(company)

with col2:
    if st.button("Clear All Companies"):
        st.session_state.selected_companies = []

# Display selected companies
st.markdown("### Selected Companies")
company_cols = st.columns(5)
for idx, company in enumerate(st.session_state.selected_companies):
    with company_cols[idx]:
        st.markdown(f"**{company}**")
        if st.button(f"Remove {company}", key=f"remove_{idx}"):
            st.session_state.selected_companies.remove(company)
            st.experimental_rerun()

# News category filter
category = st.selectbox(
    "Filter by Category",
    ["All", "Technology", "Market", "Press Releases"]
)

# Fetch and display news
if st.session_state.selected_companies:
    st.markdown("### Latest News")
    
    for company in st.session_state.selected_companies:
        st.markdown(f"#### News for {company}")
        
        try:
            news_articles = news_fetcher.fetch_news(company)
            
            if category != "All":
                news_articles = [
                    article for article in news_articles 
                    if ai_analyzer.categorize_news(article['title'])['category'] == category
                ]
            
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
                    
                    if article['url']:
                        st.markdown(f"[Read full article]({article['url']})")
        
        except Exception as e:
            st.error(f"Error fetching news for {company}: {str(e)}")

else:
    st.info("Please select at least one company to view news.")
