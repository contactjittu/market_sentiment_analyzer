"""
Gemini Summary Module
Uses Generative AI (Gemini) to generate market summaries and forecasts.
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _get_gemini_client():
    """Initialize and return Gemini client."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
    
    # Try to get available models and find one that supports generateContent
    try:
        available_models = list(genai.list_models())
        # Look for models that support generateContent
        for model in available_models:
            if hasattr(model, 'supported_generation_methods') and 'generateContent' in model.supported_generation_methods:
                # Extract model name (remove 'models/' prefix if present)
                model_name = model.name
                if model_name.startswith('models/'):
                    model_name = model_name.replace('models/', '')
                # Try to create and return the model
                try:
                    return genai.GenerativeModel(model_name)
                except Exception:
                    continue
    except Exception as e:
        # If listing models fails, try fallback names
        pass
    
    # Fallback: Try common model names in order of preference
    # Based on available models, prioritize stable "latest" versions
    model_names = [
        'gemini-flash-latest',          # Stable latest flash model
        'gemini-pro-latest',            # Stable latest pro model
        'gemini-2.5-flash',             # Current stable 2.5 flash
        'gemini-2.5-pro',               # Current stable 2.5 pro
        'gemini-2.0-flash',             # Stable 2.0 flash
        'gemini-1.5-flash-latest',
        'gemini-1.5-pro-latest', 
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            return model
        except Exception:
            continue
    
    # Last resort: use gemini-flash-latest (stable and widely available)
    return genai.GenerativeModel('gemini-flash-latest')


def generate_gemini_summary(df: pd.DataFrame) -> str:
    """
    Generate a 1-line summary of today's dominant market sentiment tone.
    
    Args:
        df: DataFrame with today's headlines (must have 'Sentiment' and 'published' columns)
    
    Returns:
        1-line summary of today's dominant tone (e.g., "Market was mostly optimistic")
    """
    if df.empty:
        return "No headlines available for today."
    
    # Count sentiment distribution
    sentiment_counts = df['Sentiment'].value_counts().to_dict()
    
    # Get sample headlines
    sample_headlines = df['title'].head(10).tolist() if 'title' in df.columns else []
    
    # Prepare prompt
    prompt = f"""Based on the following financial news headlines and sentiment distribution, provide a concise one-line summary of today's market sentiment tone.

Sentiment Distribution:
- Positive: {sentiment_counts.get('Positive', 0)}
- Negative: {sentiment_counts.get('Negative', 0)}
- Neutral: {sentiment_counts.get('Neutral', 0)}

Sample Headlines:
{chr(10).join(f"- {headline}" for headline in sample_headlines)}

Provide only a single, concise sentence summarizing the overall market sentiment tone today. Do not include any additional explanation or formatting."""

    try:
        model = _get_gemini_client()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            return f"Error: Model not available. Please check your API key and available models. Details: {error_msg}"
        return f"Error generating summary: {error_msg}"


def forecast_market_tomorrow(df: pd.DataFrame) -> str:
    """
    Generate a 1-2 sentence sentiment-based forecast for tomorrow.
    
    Args:
        df: DataFrame with today's headlines (must have 'Sentiment' and 'published' columns)
    
    Returns:
        1-2 sentence sentiment-based forecast for tomorrow
    """
    if df.empty:
        return "No headlines available to generate forecast."
    
    # Count sentiment distribution
    sentiment_counts = df['Sentiment'].value_counts().to_dict()
    
    # Get sample headlines
    sample_headlines = df['title'].head(15).tolist() if 'title' in df.columns else []
    
    # Prepare prompt
    prompt = f"""Based on the following financial news headlines and sentiment distribution from today, provide a 1-2 sentence forecast for tomorrow's market sentiment.

Sentiment Distribution:
- Positive: {sentiment_counts.get('Positive', 0)}
- Negative: {sentiment_counts.get('Negative', 0)}
- Neutral: {sentiment_counts.get('Neutral', 0)}

Sample Headlines:
{chr(10).join(f"- {headline}" for headline in sample_headlines)}

Provide a concise 1-2 sentence forecast for tomorrow's market sentiment based on today's news. Be specific and realistic."""

    try:
        model = _get_gemini_client()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            return f"Error: Model not available. Please check your API key and available models. Details: {error_msg}"
        return f"Error generating forecast: {error_msg}"


def summarize_last_5_days(data_folder: str = "news_data") -> str:
    """
    Generate a summary across the last 5 days of news headlines.
    
    Args:
        data_folder: Folder where news CSV files are stored
    
    Returns:
        Summary across last 5 days (max 50 headlines)
    """
    if not os.path.exists(data_folder):
        return "No news data folder found."
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    
    if not csv_files:
        return "No news data files found."
    
    # Parse dates from filenames and get last 5 days
    file_data = []
    for file in csv_files:
        try:
            # Assuming filename format: news_YYYY-MM-DD.csv
            date_str = file.replace('news_', '').replace('.csv', '')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            file_data.append((date_obj, file))
        except:
            continue
    
    # Sort by date and get last 5 days
    file_data.sort(key=lambda x: x[0], reverse=True)
    last_5_days_files = file_data[:5]
    
    # Collect headlines from last 5 days (max 50)
    all_headlines = []
    for date_obj, filename in last_5_days_files:
        filepath = os.path.join(data_folder, filename)
        try:
            df = pd.read_csv(filepath)
            if 'title' in df.columns:
                headlines = df['title'].tolist()
                all_headlines.extend(headlines)
        except Exception as e:
            continue
    
    # Limit to 50 headlines
    all_headlines = all_headlines[:50]
    
    if not all_headlines:
        return "No headlines found in the last 5 days."
    
    # Prepare prompt
    prompt = f"""Based on the following financial news headlines from the last 5 days, provide a comprehensive summary of the overall market sentiment and key trends.

Headlines ({len(all_headlines)} total):
{chr(10).join(f"{i+1}. {headline}" for i, headline in enumerate(all_headlines))}

Provide a detailed summary covering:
1. Overall market mood
2. Key themes and trends
3. Notable events or patterns
4. Any significant shifts in sentiment

Keep the summary informative and well-structured."""

    try:
        model = _get_gemini_client()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            return f"Error: Model not available. Please check your API key and available models. Details: {error_msg}"
        return f"Error generating historical summary: {error_msg}"

