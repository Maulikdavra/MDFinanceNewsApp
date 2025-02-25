import streamlit as st
import pandas as pd
from utils.news_fetcher import NewsFetcher
from utils.ai_analyzer import AIAnalyzer

# Page configuration
st.set_page_config(
    page_title="MDFinance",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Font Awesome integration
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)

# Initialize session state
if 'selected_companies' not in st.session_state:
    st.session_state.selected_companies = []
if 'current_company' not in st.session_state:
    st.session_state.current_company = None

def init_classes():
    return NewsFetcher(), AIAnalyzer()

news_fetcher, ai_analyzer = init_classes()

# Header
st.markdown("""
    <div class="header">
        <h1>📈 MDFinance</h1>
        <p class="subtitle">Your AI-Powered Financial News Hub</p>
    </div>
    """, unsafe_allow_html=True)

# Create two columns: left for company list, right for news
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Add Company")
    with st.form(key='add_company_form'):
        company = st.text_input("Enter a company name", key="company_input")
        submit_button = st.form_submit_button(label="Add Company")

        if submit_button and company.strip():
            if len(st.session_state.selected_companies) >= 5:
                st.warning("Maximum 5 companies can be added. Please remove some to add more.")
            elif company not in st.session_state.selected_companies:
                st.session_state.selected_companies.append(company)
                st.success(f"Added {company} to your watchlist!")
                st.rerun()
            else:
                st.warning(f"{company} is already in your watchlist!")

    if st.button("Clear All Companies"):
        st.session_state.selected_companies = []
        st.session_state.current_company = None
        st.success("Cleared all companies!")
        st.rerun()

    # Display company list with attached dustbin icons
    if st.session_state.selected_companies:
        st.markdown("### Your Companies")
        for idx, company in enumerate(st.session_state.selected_companies):
            with st.container():
                # Using HTML for better control over button and icon layout
                st.markdown(
                    f"""
                    <div class="company-container">
                        <button class="company-button {'active' if company == st.session_state.current_company else ''}"
                                onclick="parent.window.postMessage({{command: 'streamlit:setComponentValue', name: 'select_{idx}', value: true}}, '*')">
                            {company}
                        </button>
                        <button class="delete-button" title="Remove {company}"
                                onclick="parent.window.postMessage({{command: 'streamlit:setComponentValue', name: 'remove_{idx}', value: true}}, '*')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # Hidden buttons for handling clicks
                if st.button("", key=f"select_{idx}", label=company):
                    st.session_state.current_company = company
                    st.rerun()
                if st.button("", key=f"remove_{idx}"):
                    st.session_state.selected_companies.pop(idx)
                    if st.session_state.current_company == company:
                        st.session_state.current_company = None
                    st.success(f"Removed {company} from your watchlist!")
                    st.rerun()
    else:
        st.info("Add companies to your watchlist to view their news")

# Display news in the right column
with col2:
    if st.session_state.current_company:
        st.markdown(f"### Latest News for {st.session_state.current_company}")

        # News category filter
        category = st.selectbox(
            "Filter by Category",
            ["All", "Technology", "Market", "Press Releases"]
        )

        try:
            with st.spinner(f'Fetching news for {st.session_state.current_company}...'):
                news_articles = news_fetcher.fetch_news(st.session_state.current_company)

                if category != "All":
                    news_articles = [
                        article for article in news_articles 
                        if ai_analyzer.categorize_news(article['title'])['category'] == category
                    ]

                if not news_articles:
                    st.info(f"No {category.lower() if category != 'All' else ''} news found for {st.session_state.current_company}")
                else:
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
            st.error(f"Error fetching news for {st.session_state.current_company}: {str(e)}")
    else:
        st.info("Select a company from the list to view its news")