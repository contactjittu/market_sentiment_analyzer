"""
Sentiment Analyzer Module
Classifies sentiment of news headlines using VADER sentiment analysis.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Optional


def get_sentiment_analyzer() -> SentimentIntensityAnalyzer:
    """
    Returns an instance of SentimentIntensityAnalyzer from vaderSentiment.
    
    Returns:
        SentimentIntensityAnalyzer instance
    """
    return SentimentIntensityAnalyzer()


def classify_sentiment(text: str, analyzer: Optional[SentimentIntensityAnalyzer] = None) -> str:
    """
    Classify the sentiment of a news headline using VADER.
    
    Args:
        text: A news headline string
        analyzer: Instance of VADER SentimentIntensityAnalyzer (optional, will create if not provided)
    
    Returns:
        One of "Positive", "Negative", or "Neutral"
    
    Logic:
        Uses compound score:
        - ≥ 0.05 → Positive
        - ≤ -0.05 → Negative
        - else → Neutral
    """
    if analyzer is None:
        analyzer = get_sentiment_analyzer()
    
    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    
    # Classify based on compound score
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

