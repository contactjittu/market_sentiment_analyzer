"""
Visualizer Module
Plots sentiment trends by hour of the day using matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates


def plot_sentiment_line_today(df: pd.DataFrame) -> plt.Figure:
    """
    Plot a line chart showing how sentiment varies by hour of the current day.
    
    Args:
        df: DataFrame with at least 'published' (datetime) and 'Sentiment' (label) columns
    
    Returns:
        A matplotlib.figure.Figure object
    
    Logic:
        - Extract hour from published column
        - Group by hour and sentiment
        - Plot line chart with 3 lines (Positive, Negative, Neutral)
        - X-axis: 0 to 23 hours
        - Y-axis: count of headlines
    """
    # Make a copy to avoid modifying original dataframe
    df_copy = df.copy()
    
    # Ensure published is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_copy['published']):
        df_copy['published'] = pd.to_datetime(df_copy['published'])
    
    # Extract hour from published column
    df_copy['hour'] = df_copy['published'].dt.hour
    
    # Group by hour and sentiment, count headlines
    sentiment_counts = df_copy.groupby(['hour', 'Sentiment']).size().reset_index(name='count')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Get unique sentiment values
    sentiments = ['Positive', 'Negative', 'Neutral']
    colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
    
    # Plot line for each sentiment
    for sentiment in sentiments:
        sentiment_data = sentiment_counts[sentiment_counts['Sentiment'] == sentiment]
        if not sentiment_data.empty:
            ax.plot(sentiment_data['hour'], sentiment_data['count'], 
                   marker='o', label=sentiment, color=colors.get(sentiment, 'blue'), linewidth=2)
    
    # Set labels and title
    ax.set_xlabel('Hour of Day (24h)', fontsize=12)
    ax.set_ylabel('Headline Count', fontsize=12)
    ax.set_title('Live Market Sentiment Trend (Hourly Today)', fontsize=14, fontweight='bold')
    
    # Set x-axis to show all hours (0-23)
    ax.set_xlim(-0.5, 23.5)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(loc='best', fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

