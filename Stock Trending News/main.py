from datetime import datetime, timedelta
from twilio.rest import Client
import requests

# Define constants for the stock symbol and company name
STOCK = "TSLA"  # Stock symbol for Tesla
COMPANY_NAME = "Tesla Inc"

# API keys for accessing stock price data and news data
stock_api = "your apikey given from Alpha"  # API key for Alpha Vantage
news_api = "your apikey given from nesapi"  # API key for NewsAPI

# Endpoints for the APIs
STOCK_ENDPOINT = "https://www.alphavantage.co/query"  # Alpha Vantage endpoint
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"  # NewsAPI endpoint

# Parameters for the stock data request
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api
}

# Make a request to the stock data API
response = requests.get(STOCK_ENDPOINT, params=params)
data = response.json()

# Calculate the dates for yesterday and the day before yesterday
today = datetime.now().date()
yesterday = today - timedelta(days=2)
two_day_ago = yesterday - timedelta(days=1)

# Get the closing prices for yesterday and the day before yesterday
yesterday_closing = data["Time Series (Daily)"][str(yesterday)]["4. close"]
two_day_ago_closing = data["Time Series (Daily)"][str(two_day_ago)]["4. close"]

# Calculate the difference in closing prices
difference = float(yesterday_closing) - float(two_day_ago_closing)

# Determine if the stock went up or down
up_down = "🔺" if difference > 0 else "🔻"

# Calculate the percentage difference
diff_percent = round((difference / float(yesterday_closing)) * 100)

# If the percentage difference is greater than 1, fetch news articles
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": news_api,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    # Format the articles for the message body
    formatted_articles = [
        f"{STOCK} {up_down} Headline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles
    ]

    # Twilio account credentials
    account_sid = 'your account sid given from twilio'
    auth_token = 'your token given from twilio'
    client = Client(account_sid, auth_token)

    # Send each formatted article as an SMS
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='demo number given from twilio',
            to='yoru number'
        )


