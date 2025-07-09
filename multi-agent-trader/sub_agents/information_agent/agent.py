from pydantic import BaseModel
from google.adk.agents import ParallelAgent, Agent
from ..market_agent import market_agent
from ..sentiment_agent import sentiment_agent
from ..fundamentals_agent import fundamentals_agent

information_agent = ParallelAgent(
    name="information_retriever",
    sub_agents=[market_agent, fundamentals_agent, sentiment_agent],
    description="Agent to gather relevant information about a specifed stock",
    # instruction="""
    # You are a parallel agent responsible for gathering investment-related information on a specific stock ticker. 

    # You will run the following sub-agents simultaneously:
    # - The market agent retrieves current technical indicators such as price, volume, RSI, and moving averages.
    # - The fundamentals agent provides macroeconomic insights and financial statement highlights for the company.
    # - The sentiment agent analyzes recent news, social media, or financial commentary to determine public sentiment.

    # Collect all results and return them together as a unified response for downstream agents to use.
    # """
)