"""
Market Sentiment Analyzer - Main Application
Streamlit application for analyzing financial news sentiment.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.news_fetcher import fetch_google_news
from utils.sentiment_analyzer import get_sentiment_analyzer, classify_sentiment
from utils.visualizer import plot_sentiment_line_today
from utils.gemini_summary import generate_gemini_summary, forecast_market_tomorrow, summarize_last_5_days


def ensure_data_folder():
    """Ensure news_data folder exists."""
    data_folder = "news_data"
    os.makedirs(data_folder, exist_ok=True)
    return data_folder


def get_today_filename(data_folder: str) -> str:
    """Get today's CSV filename."""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(data_folder, f"news_{today}.csv")

def load_existing_news(data_folder: str) -> pd.DataFrame:
    """Load existing news from today's file if it exists."""
    filename = get_today_filename(data_folder)
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            # Convert published to datetime if it's not already
            if 'published' in df.columns:
                df['published'] = pd.to_datetime(df['published'])
            return df
        except Exception as e:
            st.warning(f"Error loading existing file: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def save_news_to_csv(news_list: list, data_folder: str) -> int:
    """
    Save news headlines to CSV, avoiding duplicates.
    Returns the number of new headlines added.
    """
    if not news_list:
        return 0
    
    # Load existing news
    existing_df = load_existing_news(data_folder)
    
    # Create new dataframe from news list
    new_df = pd.DataFrame(news_list)
    
    # Convert published to datetime
    if 'published' in new_df.columns:
        new_df['published'] = pd.to_datetime(new_df['published'])
    
    # Add sentiment analysis
    analyzer = get_sentiment_analyzer()
    new_df['Sentiment'] = new_df['title'].apply(
        lambda x: classify_sentiment(x, analyzer)
    )
    
    # Remove duplicates based on title
    if not existing_df.empty and 'title' in existing_df.columns:
        existing_titles = set(existing_df['title'].tolist())
        new_df = new_df[~new_df['title'].isin(existing_titles)]
    
    # Combine with existing data
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    # Save to CSV
    filename = get_today_filename(data_folder)
    combined_df.to_csv(filename, index=False)
    
    return len(new_df)


def cleanup_old_files(data_folder: str, days_threshold: int = 90):
    """Delete news files older than specified days (default 3 months = 90 days)."""
    if not os.path.exists(data_folder):
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_threshold)
    deleted_count = 0
    
    for filename in os.listdir(data_folder):
        if filename.startswith('news_') and filename.endswith('.csv'):
            try:
                # Extract date from filename
                date_str = filename.replace('news_', '').replace('.csv', '')
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                if file_date < cutoff_date:
                    filepath = os.path.join(data_folder, filename)
                    os.remove(filepath)
                    deleted_count += 1
            except Exception as e:
                # Skip files with invalid names
                continue
    
    return deleted_count


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Market Sentiment Analyzer",
        page_icon="📈",
        layout="wide"
    )
    
    st.title("📈 Market Sentiment Analyzer")
    st.markdown("Analyze real-time financial news sentiment and generate market insights")
    
    # Ensure data folder exists
    data_folder = ensure_data_folder()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        query = st.text_input("Search Query", value="stock market", help="Enter search term for Google News")
        
        if st.button("Fetch Latest News", type="primary"):
            with st.spinner("Fetching news..."):
                try:
                    news_list = fetch_google_news(query)
                    if news_list:
                        new_count = save_news_to_csv(news_list, data_folder)
                        st.success(f"Fetched {len(news_list)} headlines. {new_count} new headlines added.")
                    else:
                        st.warning("No news found for the query.")
                except Exception as e:
                    st.error(f"Error fetching news: {e}")
        
        # Cleanup old files
        if st.button("Cleanup Old Files"):
            with st.spinner("Cleaning up..."):
                deleted = cleanup_old_files(data_folder)
                st.success(f"Deleted {deleted} old files (> 3 months)")
    
    # Load today's data
    df = load_existing_news(data_folder)
    
    if df.empty:
        st.info("👆 Fetch some news using the sidebar to get started!")
        return
    
    # Display statistics
    st.header("📊 Today's Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Headlines", len(df))
    
    with col2:
        positive_count = len(df[df['Sentiment'] == 'Positive'])
        st.metric("Positive", positive_count)
    
    with col3:
        negative_count = len(df[df['Sentiment'] == 'Negative'])
        st.metric("Negative", negative_count)
    
    with col4:
        neutral_count = len(df[df['Sentiment'] == 'Neutral'])
        st.metric("Neutral", neutral_count)
    
    st.info(f"Stored {len(df)} unique headlines in today's file.")
    
    # Visualization
    st.header("📈 Sentiment Trend – Line Plot")
    if 'published' in df.columns and 'Sentiment' in df.columns:
        try:
            fig = plot_sentiment_line_today(df)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error creating visualization: {e}")
    else:
        st.warning("Missing required columns for visualization.")
    
    # Gemini Summary Section
    st.header("🤖 Gemini Summary")
    
    if st.button("Generate Summary", key="summary"):
        with st.spinner("Generating summary..."):
            try:
                summary = generate_gemini_summary(df)
                st.write(summary)
            except Exception as e:
                st.error(f"Error generating summary: {e}")
    
    # Tomorrow's Forecast
    st.header("🔮 Tomorrow's Forecast (Sentiment-based)")
    
    if st.button("Generate Forecast", key="forecast"):
        with st.spinner("Generating forecast..."):
            try:
                forecast = forecast_market_tomorrow(df)
                st.write(forecast)
            except Exception as e:
                st.error(f"Error generating forecast: {e}")
    
    # Historical Summary
    st.header("📚 Historical Summary (Last 5 Days)")
    
    if st.button("Generate Historical Summary", key="historical"):
        with st.spinner("Generating historical summary..."):
            try:
                historical_summary = summarize_last_5_days(data_folder)
                st.write(historical_summary)
            except Exception as e:
                st.error(f"Error generating historical summary: {e}")
    
    # Display raw data (optional)
    with st.expander("View Raw Data"):
        st.dataframe(df)


if __name__ == "__main__":
    # Auto-cleanup on startup
    data_folder = ensure_data_folder()
    cleanup_old_files(data_folder)
    
    # Run Streamlit app
    main()

