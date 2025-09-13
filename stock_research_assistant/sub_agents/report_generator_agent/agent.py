from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent

# Define the schemas for each section of the report.
# This ensures a well-structured and consistent output.
class FundamentalsSection(BaseModel):
    valuation_summary: str = Field(description="A descriptive paragraph summarizing key valuation metrics (e.g., P/E, P/S, market cap) and financial health.")
    key_metrics: dict = Field(description="A dictionary of key fundamental metrics like EPS, P/E, Market Cap, etc.")

class TechnicalsSection(BaseModel):
    market_overview: str = Field(description="A descriptive paragraph summarizing the stock's recent price action and overall market trends.")
    key_indicators: dict = Field(description="A dictionary of key technical indicators like RSI, Moving Averages (MA), etc.")

class SentimentSection(BaseModel):
    sentiment_summary: str = Field(description="A descriptive paragraph summarizing the latest news, social media, and analyst sentiment for the stock.")

class Report(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL).")
    report_title: str = Field(description="A concise, descriptive title for the investor report.")
    fundamentals: FundamentalsSection
    technicals: TechnicalsSection
    sentiment: SentimentSection
    conclusion: str = Field(description="A concluding summary of the research, highlighting key insights and potential risks.")
    
report_generator = LlmAgent(
    name="report_generator_agent",
    model="gemini-1.5-pro",
    description="Agent that aggregates inputs from other agents and generates a comprehensive investor report in a structured format.",
    output_schema=Report,
    instruction="""
    You are an AI financial report writer. Your task is to take detailed summaries from a team of expert agents and synthesize them into a single, cohesive, and professional investor report.

    You will receive the following inputs:

    * **Fundamental Data:**
    {stock_data_agent_result}

    * **Market and Technical Data:**
    {market_data_agent_result}
    
    * **Sentiment Analysis:**
    {sentiment_agent_result}

    Use only the information provided in the inputs to fill the `Report` schema. Your goal is to combine the data into a high-quality, readable narrative within each section's summary field. 
    Do not invent or assume any information. Your output must conform exactly to the `Report` schema.
    """,
    output_key="investor_report"
)