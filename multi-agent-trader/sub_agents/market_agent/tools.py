from google.adk.tools import Tool
import yfinance as yf
import requests

# Replace this with your real API logic
def fetch_stock_data(ticker: str) -> str:
    return f"Fake stock data for {ticker}: price=172.35, RSI=29.3"

get_stock_data = Tool(
    name="get_stock_data",
    description="Fetches current stock price, RSI, and other indicators for a given ticker symbol.",
    inputs={"ticker": str},
    func=fetch_stock_data,
)