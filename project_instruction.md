Project Question

Title: Market Sentiment Analyzer

Problem Statement:

In today’s fast-paced financial world, investors and analysts rely heavily on the tone of real-time market news to gauge the mood of the economy and make informed decisions. Your task is to build a Market Sentiment Analyzer that fetches live financial news, classifies the sentiment of each headline, visualizes sentiment trends, and uses Generative AI to generate concise market summaries and forecasts.
This project involves integrating RSS-based news feeds, VADER sentiment analysis, matplotlib-based visualization, and LLM-powered summaries and predictions.

Objective:

Build a modular Streamlit application that:
Fetches financial news headlines from Google News RSS.
Performs sentiment analysis (Positive / Negative / Neutral) on each headline.
Stores daily headlines in CSV files (avoiding duplicates).
Visualizes hour-wise sentiment trends for the current day.
Generates a one-line summary, tomorrow’s forecast, and a 5-day historical sentiment summary using any Generative AI model (e.g., Gemini, GPT-3.5, Azure GPT).
Automatically deletes old news files (> 3 months).

Instructions:

You are provided with a main.py that handles UI, orchestration, and file cleanup.
You are required to implement logic inside the following modular Python files in the utils/ directory:
gemini_summary.py
news_fetcher.py
sentiment_analyzer.py
visualizer.py

File Structure:
Project/
├── news_data/
├── utils/
│ ├── gemini_summary.py
│ ├── news_fetcher.py
│ ├── sentiment_analyzer.py
│ └── visualizer.py
├── .env
├── installation.txt
├── main.py
└── tests.py

utils/news_fetcher.py:
Purpose: Fetch real-time financial news headlines from the Google News RSS feed based on a given search query.
Function to implement: def fetch_google_news(query: str = "stock market") -> list
Input: query (a string keyword, e.g., "stock market" or "nifty")
Output: Returns a list of dictionaries. Each dictionary should have:

"source" (always "Google News")
"title" (news headline)
"link" (news link)
"published" (timestamp string)
Example:
[
    {
        "source": "Google News",
        "title": "Stocks rally as inflation cools",
        "link": "https://news.google.com/article/...",
        "published": "Tue, 18 Jun 2025 10:00:00 GMT"
    },
...
]

utils/sentiment_analyzer.py:
Purpose: Classify the sentiment of each headline using VADER. This helps assess if news is positive, negative, or neutral.
Functions to implement:
def get_sentiment_analyzer() -> SentimentIntensityAnalyzer:
    Returns an instance of SentimentIntensityAnalyzer (from vaderSentiment)

def classify_sentiment(text: str, analyzer: SentimentIntensityAnalyzer) -> str:

Input: text (a news headline), analyzer (instance of VADER analyzer)

Output: One of "Positive", "Negative", or "Neutral"

Logic Guide: Use the compound score:
≥ 0.05 → Positive
≤ -0.05 → Negative
else → Neutral

utils/gemini_summary.py:
Purpose: Use any GenAI model (e.g., Gemini, Azure GPT, OpenAI) to summarize today’s sentiment, forecast tomorrow, and summarize past 5 days.
Functions to implement:

def generate_gemini_summary(df: pd.DataFrame) -> str:
Input: DataFrame with today’s headlines (must have Sentiment, published)
Output: 1-line summary of today’s dominant tone (e.g., "Market was mostly optimistic")

def forecast_market_tomorrow(df: pd.DataFrame) -> str:
Input: Same DataFrame
Output: 1–2 sentence sentiment-based forecast for tomorrow (e.g., "Based on current headlines, markets may remain bullish")

def summarize_last_5_days(data_folder: str = "news_data") -> str:
Input: Folder where news CSVs are stored
Output: Summary across last 5 days (max 50 headlines)

Notes: You can use any GenAI provider. Prompt content and model name are not evaluated.

utils/visualizer.py:
Purpose: Plot a line chart showing how sentiment varies by hour of the current day.
Function to implement: def plot_sentiment_line_today(df: pd.DataFrame):

Input: DataFrame with at least published (datetime) and Sentiment (label)

Output: A matplotlib.figure.Figure object

Logic Guide: Extract hour from published column, group by hour and sentiment, plot line chart with 3 lines (Positive, Negative, Neutral).
X-axis: 0 to 23 hours
Y-axis: count of headlines

Sample Expected Outputs:
Sentiment Summary (Today): "The market tone today was largely positive, especially during mid-day hours."
Forecast (Tomorrow): "Based on today’s optimism, markets may open strong tomorrow unless new economic data shifts sentiment."

Commands to Create a Google Gemini API Key:

Launch any browser (e.g., Chrome, Firefox) on your computer.

Go to Google AI Studio. type aistudio.google.com

Sign in to your Google account.
Click the "Sign In" button in the top-right corner.
Enter your Google email and password, then click "Next" to log in.
If you don’t have an account, click "Create Account" and follow the prompts to make one.
Navigate to the API Key section:
On the Google AI Studio homepage, look at the left sidebar.
Click on "Get API Key" (usually near the top-left corner).
Create a new API key:
In the API Key section, click the "Create API Key" button.
A pop-up will appear—select "Create API Key in new project" (or choose an existing project if you have one).
Click "Create" to generate the key.
Copy the generated API key:
Once the key is created, it will appear on the screen.
Click the "Copy" button next to the key (or highlight it and press Ctrl+C/Command+C).
Save the key in a secure place (e.g., a text file or password manager) because it won’t be shown again.


Implementation Explanation:

Before executing the main.py, enter the Gemini API key in the .env file.
Open the main.py integrated terminal.
Check the path in the Project directory, if not use cd command to navigate.
To install required packages, run python3 main.py in terminal or click the run & debug button for main.py.
Use python3 -m streamlit run main.py to execute the application, then you will get the pop-up window below, click the associate port (Open in Browser) which will navigate to streamlit application window.

```
You can now view your Streamlit app in your browser:
Local URL: http://localhost:8501/
Network URL: http://10.240.24.182:8501/
External URL: http://20.240.245.156:8501/
```

To check the testcases, you can use python3 -W ignore -m pytest tests.py -v (check the directory it should be Project directory).


Sample Output:

Market Sentiment Analyzer
Stored 107 unique headlines in today’s file.

Sentiment Trend – Line Plot
Live Market Sentiment Trend (Hourly Today)
(X-axis: Hour of Day 24h, Y-axis: Headline Count, 3 lines for Sentiment: Positive, Negative, Neutral)


Gemini Summary

Market sentiment is overwhelmingly positive, with a significant skew towards positive headlines; peak news activity occurred at 8:30 PM IST.

Tomorrow’s Forecast (Sentiment-based)

Short-Term Market Sentiment: Slightly Negative to Neutral

Based on the news headlines, here’s a breakdown of the sentiment:

Positive Factors:

Indian indices showed some upward movement during the day, although closing lower.
Tel Aviv stock exchange jumps despite attack.
Oswal Pumps IPO listing expected at a premium.
Power sector as an opportunity.

Negative Factors:

US Futures drop.
S&P 500 closed lower.
Indian indices closed lower for the 3rd day due to geopolitical tensions.
Potential for stagflation in the U.S. impacting Indian markets.
Geopolitical tensions (Israel-Iran) and their potential impact.
Valuation concerns expressed by analysts.
Aten Papers shares made a muted debut.
Sun TV shares slide.


Historical Summary (Last 5 Days)

Overall, the market mood over the last 5 days appears to be cautious and somewhat negative, with a high degree of volatility influenced by geopolitical tensions and macroeconomic concerns. Here’s a breakdown:
Geopolitical Uncertainty: The dominant theme is the Israel-Iran conflict, creating significant market jitters. While the Tel Aviv stock exchange surprisingly surged despite an attack, the broader impact is reflected in falling Dow futures and cautious trading elsewhere.
Domestic Market Performance: Indian markets generally closed lower for multiple days, particularly impacting mid and small-cap stocks, leading to investor losses. There were some positive openings, but the gains were not sustained.
Global Economic Concerns: The US Federal Reserve’s stance on interest rates, coupled with rising stagflation fears, adds to the negative sentiment. Concerns about valuations and fresh equity supply are also weighing on the Indian market.
Mixed Individual Stock Performance: While some IPOs like Oswal Pumps debuted at a premium, others like Aten Papers & Foam had a muted or negative entry. There are ongoing recommendations for specific stocks to buy, suggesting some optimism in certain sectors.
US Market Holidays: Mentions of the US stock market being closed for Juneteenth highlight the global interconnectedness and the impact of events in one market on others.
Sectoral Variances: Some sectors, like autos, outperformed despite the overall market decline, while others, like mining, saw gains on specific days.

Note:
The project will not be submitted if "Submit Project" is not done at least once.