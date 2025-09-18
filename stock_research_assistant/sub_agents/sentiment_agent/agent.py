from google.adk.agents import LlmAgent
from google.adk.tools import google_search

sentiment_agent = LlmAgent(
    name="stock_sentiment_agent",
    model="gemini-2.0-flash",
    description="Agent to gather current sentiment around a specific stock.",
    instruction="""
    You are a market sentiment assistant. Your role is to provide up-to-date sentiment about a certain stock.

    You can use the `google_search` tool to look through social media platforms like X, Reddit, Stocktwits, or 
    credible analyst reports if available to achieve a sentiment.
    """,
    tools=[google_search],
    output_key="sentiment_agent_result",
)
