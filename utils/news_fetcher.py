"""
News Fetcher Module
Fetches real-time financial news headlines from Google News RSS feed.
"""

import feedparser
from typing import List, Dict
from urllib.parse import quote_plus


def fetch_google_news(query: str = "stock market") -> List[Dict]:
    """
    Fetch real-time financial news headlines from Google News RSS feed.
    
    Args:
        query: A string keyword for news search (e.g., "stock market" or "nifty")
    
    Returns:
        A list of dictionaries, each containing:
        - "source": "Google News"
        - "title": news headline
        - "link": news link
        - "published": timestamp string
    """
    # URL-encode the query parameter to handle spaces and special characters
    encoded_query = quote_plus(query)
    # Construct Google News RSS URL
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    news_list = []
    
    # Extract news items
    for entry in feed.entries:
        news_item = {
            "source": "Google News",
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", "")
        }
        news_list.append(news_item)
    
    return news_list

