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

# Initialize session state for companies
if 'selected_companies' not in st.session_state:
    st.session_state.selected_companies = []

def init_classes():
    return NewsFetcher(), AIAnalyzer()

news_fetcher, ai_analyzer = init_classes()

# Header
st.title("📰 AI-Powered News Aggregator")
st.markdown("### Stay informed about your favorite companies")

# Company selection
company = st.text_input("Enter a company name", key="company_input")
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Add Company", key="add_company"):
        if company.strip():  # Check if company name is not empty
            if len(st.session_state.selected_companies) >= 5:
                st.warning("Maximum 5 companies can be added. Please remove some to add more.")
            elif company not in st.session_state.selected_companies:
                st.session_state.selected_companies.append(company)
                st.success(f"Added {company} to your watchlist!")
                st.rerun()
            else:
                st.warning(f"{company} is already in your watchlist!")

with col2:
    if st.button("Clear All Companies"):
        st.session_state.selected_companies = []
        st.success("Cleared all companies!")
        st.rerun()

# Display selected companies
if st.session_state.selected_companies:
    st.markdown("### Selected Companies")
    cols = st.columns(len(st.session_state.selected_companies))
    for idx, company in enumerate(st.session_state.selected_companies):
        with cols[idx]:
            st.markdown(f"**{company}**")
            if st.button(f"Remove", key=f"remove_{idx}"):
                st.session_state.selected_companies.pop(idx)
                st.success(f"Removed {company} from your watchlist!")
                st.rerun()

# News category filter
if st.session_state.selected_companies:
    category = st.selectbox(
        "Filter by Category",
        ["All", "Technology", "Market", "Press Releases"]
    )

    # Fetch and display news
    st.markdown("### Latest News")

    for company in st.session_state.selected_companies:
        st.markdown(f"#### News for {company}")

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
                    continue

                for article in news_articles:
                    with st.expander(article['title']):
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.markdown(f"**Source:** {article['source']}")
                            st.markdown(f"**Published:** {article['publishedAt']}")
                            st.markdown("**Summary:**")
                            try:
                                summary = ai_analyzer.summarize_news(article['description'])
                                st.write(summary)
                            except Exception as e:
                                st.warning("Could not generate summary. Using original description.")
                                st.write(article['description'])

                        with col2:
                            try:
                                sentiment = ai_analyzer.analyze_sentiment(article['description'])
                                st.markdown("**Sentiment Analysis:**")
                                st.progress(sentiment['confidence'])
                                st.markdown(f"Rating: {'⭐' * sentiment['rating']}")
                            except Exception as e:
                                st.info("Sentiment analysis unavailable")

                        if article['url']:
                            st.markdown(f"[Read full article]({article['url']})")

        except Exception as e:
            st.error(f"Error fetching news for {company}: {str(e)}")
else:
    st.info("Please add a company to view news.")