from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from .sub_agents.stock_data_agent import stock_data_agent
from .sub_agents.sentiment_agent import sentiment_agent
from .sub_agents.report_generator_agent import report_generator
from .sub_agents.nlp_screener_agent import nlp_screener_agent

root_agent = LlmAgent(
    name="stock_research_assistant",
    description="A comprehensive assistant for analyzing stocks, market trends, and news sentiment to generate in-depth investor reports.",
    model="gemini-2.5-pro",
    tools=[
        AgentTool(agent=stock_data_agent),
        AgentTool(agent=sentiment_agent),
        AgentTool(agent=report_generator, skip_summarization=True), # keep report format
    ],
    instruction="""
    You are an expert AI Stock Research Assistant. Your primary goal is to help users
    conduct thorough, data-backed research on publicly traded companies.

    Your responsibilities include:
    - Answering questions about stock fundamentals, pricing, and technical indicators.
    - Analyzing news and social media to provide a sentiment overview.
    - Screening for stocks that match a user's natural language criteria.
    - Generating structured investor reports that summarize all available information.

    **Do not provide financial advice, and do not execute trades.**
    Use your tools to fulfill user requests, and always aim to provide clear, actionable insights in your final response.
    If a query is outside the scope of stock research, politely inform the user of your purpose.
    """
)