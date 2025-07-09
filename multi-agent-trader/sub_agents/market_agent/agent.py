from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .tools import get_stock_data
from pydantic import BaseModel, Field

market_agent = LlmAgent(
    name="stock_information_agent",
    model="gemini-2.0-flash",
    description="Agent to gather current and historical stock data for a given ticker.",
    instruction="""
    You are a market data assistant. Your role is to gather accurate and up-to-date information about publicly traded stocks.

    Given a ticker symbol (e.g., AAPL for Apple, TSLA for Tesla), gather and summarize common stock information

    You can use the `google_search` tool to find pages like Yahoo Finance or MarketWatch for this information.
    """,
    tools=[google_search],
    output_key="market_agent_result",
)
