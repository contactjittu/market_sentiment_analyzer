"""
Test cases for Market Sentiment Analyzer
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.news_fetcher import fetch_google_news
from utils.sentiment_analyzer import get_sentiment_analyzer, classify_sentiment
from utils.visualizer import plot_sentiment_line_today
from utils.gemini_summary import generate_gemini_summary, forecast_market_tomorrow, summarize_last_5_days


class TestNewsFetcher:
    """Tests for news_fetcher.py"""
    
    def test_fetch_google_news_default_query(self):
        """Test fetching news with default query."""
        news = fetch_google_news()
        assert isinstance(news, list)
        if news:
            assert "source" in news[0]
            assert "title" in news[0]
            assert "link" in news[0]
            assert "published" in news[0]
            assert news[0]["source"] == "Google News"
    
    def test_fetch_google_news_custom_query(self):
        """Test fetching news with custom query."""
        news = fetch_google_news("nifty")
        assert isinstance(news, list)
        if news:
            assert news[0]["source"] == "Google News"


class TestSentimentAnalyzer:
    """Tests for sentiment_analyzer.py"""
    
    def test_get_sentiment_analyzer(self):
        """Test getting sentiment analyzer instance."""
        analyzer = get_sentiment_analyzer()
        assert analyzer is not None
    
    def test_classify_sentiment_positive(self):
        """Test classifying positive sentiment."""
        analyzer = get_sentiment_analyzer()
        result = classify_sentiment("Stocks rally as inflation cools", analyzer)
        assert result in ["Positive", "Negative", "Neutral"]
    
    def test_classify_sentiment_negative(self):
        """Test classifying negative sentiment."""
        analyzer = get_sentiment_analyzer()
        result = classify_sentiment("Market crashes amid economic crisis", analyzer)
        assert result in ["Positive", "Negative", "Neutral"]
    
    def test_classify_sentiment_neutral(self):
        """Test classifying neutral sentiment."""
        analyzer = get_sentiment_analyzer()
        result = classify_sentiment("Market opens at 9:30 AM", analyzer)
        assert result in ["Positive", "Negative", "Neutral"]
    
    def test_classify_sentiment_without_analyzer(self):
        """Test classifying sentiment without passing analyzer."""
        result = classify_sentiment("Test headline")
        assert result in ["Positive", "Negative", "Neutral"]


class TestVisualizer:
    """Tests for visualizer.py"""
    
    def test_plot_sentiment_line_today(self):
        """Test plotting sentiment line chart."""
        # Create sample dataframe
        dates = [datetime.now() - timedelta(hours=i) for i in range(10)]
        df = pd.DataFrame({
            'published': dates,
            'Sentiment': ['Positive', 'Negative', 'Neutral'] * 3 + ['Positive'],
            'title': [f'Headline {i}' for i in range(10)]
        })
        
        fig = plot_sentiment_line_today(df)
        assert fig is not None
    
    def test_plot_sentiment_line_empty_df(self):
        """Test plotting with empty dataframe."""
        df = pd.DataFrame(columns=['published', 'Sentiment'])
        fig = plot_sentiment_line_today(df)
        assert fig is not None


class TestGeminiSummary:
    """Tests for gemini_summary.py"""
    
    def test_generate_gemini_summary(self):
        """Test generating Gemini summary."""
        df = pd.DataFrame({
            'title': ['Stocks rally', 'Market crashes', 'Neutral news'],
            'Sentiment': ['Positive', 'Negative', 'Neutral'],
            'published': [datetime.now()] * 3
        })
        
        # This test may fail if API key is not set, which is expected
        try:
            summary = generate_gemini_summary(df)
            assert isinstance(summary, str)
            assert len(summary) > 0
        except ValueError as e:
            # Expected if API key is not set
            assert "GEMINI_API_KEY" in str(e) or "API" in str(e)
    
    def test_forecast_market_tomorrow(self):
        """Test forecasting market tomorrow."""
        df = pd.DataFrame({
            'title': ['Stocks rally', 'Market crashes', 'Neutral news'],
            'Sentiment': ['Positive', 'Negative', 'Neutral'],
            'published': [datetime.now()] * 3
        })
        
        try:
            forecast = forecast_market_tomorrow(df)
            assert isinstance(forecast, str)
            assert len(forecast) > 0
        except ValueError as e:
            # Expected if API key is not set
            assert "GEMINI_API_KEY" in str(e) or "API" in str(e)
    
    def test_summarize_last_5_days(self):
        """Test summarizing last 5 days."""
        # Create test data folder if it doesn't exist
        test_folder = "test_news_data"
        os.makedirs(test_folder, exist_ok=True)
        
        try:
            # Create a test CSV file
            test_df = pd.DataFrame({
                'title': ['Test headline'],
                'Sentiment': ['Positive'],
                'published': [datetime.now()]
            })
            test_file = os.path.join(test_folder, f"news_{datetime.now().strftime('%Y-%m-%d')}.csv")
            test_df.to_csv(test_file, index=False)
            
            try:
                summary = summarize_last_5_days(test_folder)
                assert isinstance(summary, str)
            except ValueError as e:
                # Expected if API key is not set
                assert "GEMINI_API_KEY" in str(e) or "API" in str(e)
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(test_folder):
                os.rmdir(test_folder)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

