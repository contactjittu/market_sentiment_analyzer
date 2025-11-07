# How to Run and Test Market Sentiment Analyzer

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Internet connection (for fetching news and using Gemini API)

## Step 1: Install Dependencies

Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install streamlit pandas feedparser vaderSentiment matplotlib python-dotenv google-generativeai pytest
```

## Step 2: Set Up Gemini API Key

1. **Get your API key:**
   - Go to https://aistudio.google.com
   - Sign in with your Google account
   - Click "Get API Key" in the left sidebar
   - Click "Create API Key" → "Create API Key in new project"
   - Copy the generated API key

2. **Add API key to .env file:**
   - Open the `.env` file in the project root
   - Replace `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   - Save the file

## Step 3: Run the Application

### Option A: Using Streamlit (Recommended)

```bash
python3 -m streamlit run main.py
```

The application will:
- Automatically open in your browser at `http://localhost:8501`
- Display URLs in the terminal if auto-open doesn't work:
  - Local URL: http://localhost:8501/
  - Network URL: (your network IP)

### Option B: Run main.py directly (for installation check)

```bash
python3 main.py
```

This will check if dependencies are installed and create necessary folders.

## Step 4: Using the Application

1. **In the Streamlit app:**
   - Use the sidebar to enter a search query (default: "stock market")
   - Click "Fetch Latest News" to get headlines
   - View statistics and sentiment trends
   - Click buttons to generate:
     - Gemini Summary
     - Tomorrow's Forecast
     - Historical Summary (Last 5 Days)

2. **Features:**
   - News is automatically saved to `news_data/` folder
   - Duplicate headlines are automatically filtered
   - Old files (> 3 months) are auto-deleted on startup

## Step 5: Run Tests

Run all test cases:

```bash
python3 -W ignore -m pytest tests.py -v
```

Run specific test classes:

```bash
# Test news fetcher
python3 -W ignore -m pytest tests.py::TestNewsFetcher -v

# Test sentiment analyzer
python3 -W ignore -m pytest tests.py::TestSentimentAnalyzer -v

# Test visualizer
python3 -W ignore -m pytest tests.py::TestVisualizer -v

# Test Gemini summary (requires API key)
python3 -W ignore -m pytest tests.py::TestGeminiSummary -v
```

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
- **Solution:** Make sure `.env` file exists and contains your API key
- Check that `python-dotenv` is installed

### Issue: "Module not found"
- **Solution:** Install missing packages: `pip install -r requirements.txt`

### Issue: "Port 8501 already in use"
- **Solution:** Streamlit will automatically use the next available port, or stop the other process

### Issue: "No news found"
- **Solution:** Check your internet connection and try a different search query

### Issue: Tests fail for Gemini functions
- **Solution:** This is expected if API key is not set. Tests will check for proper error handling.

## Project Structure

```
market_sentiment_analyzer/
├── news_data/              # CSV files with daily news (auto-created)
├── utils/                  # Utility modules
│   ├── gemini_summary.py
│   ├── news_fetcher.py
│   ├── sentiment_analyzer.py
│   └── visualizer.py
├── .env                    # API key configuration
├── main.py                 # Main Streamlit application
├── tests.py                # Test cases
└── requirements.txt        # Python dependencies
```

## Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit .env file with your API key
# (Use your preferred editor)

# 3. Run the application
python3 -m streamlit run main.py

# 4. Run tests (in another terminal)
python3 -W ignore -m pytest tests.py -v
```

## Expected Output

When running the application, you should see:
- Streamlit app opens in browser
- Sidebar with search and fetch options
- Statistics showing total headlines and sentiment counts
- Line chart showing hourly sentiment trends
- Buttons to generate AI summaries and forecasts

When running tests, you should see:
- Test results for each module
- Pass/fail status for each test
- Some tests may be skipped if API key is not configured (expected behavior)

