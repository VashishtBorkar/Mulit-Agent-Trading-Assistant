from pydantic import BaseModel, Field
from typing import Optional, Dict
from google.adk.agents import LlmAgent

# Define the schemas for each section of the report.
# This ensures a well-structured and consistent output.
class FundamentalsSection(BaseModel):
    valuation_summary: str = Field(description="A descriptive paragraph summarizing key valuation metrics (e.g., P/E, P/S, market cap) and financial health.")
    key_metrics: Dict[str, str] = Field(description="A dictionary of key fundamental metrics like EPS, P/E, Market Cap, etc.")
    extra_notes: Optional[str] = Field(
        default=None,
        description="Any additional insights, metrics, or commentary that do not fit into the other fields."
    )

class TechnicalsSection(BaseModel):
    market_overview: str = Field(description="A descriptive paragraph summarizing the stock's recent price action and overall market trends.")
    key_indicators: Dict[str, str] = Field(description="A dictionary of key technical indicators like RSI, Moving Averages (MA), etc.")
    extra_notes: Optional[str] = Field(
        default=None,
        description="Any additional insights, metrics, or commentary that do not fit into the other fields."
    )

class SentimentSection(BaseModel):
    sentiment_summary: str = Field(description="A descriptive paragraph summarizing the latest news, social media, and analyst sentiment for the stock.")
    extra_notes: Optional[str] = Field(
        default=None,
        description="Any additional insights, metrics, or commentary that do not fit into the other fields."
    )

class Report(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL).")
    report_title: str = Field(description="A concise, descriptive title for the investor report.")
    fundamentals: FundamentalsSection
    technicals: TechnicalsSection
    sentiment: SentimentSection
    conclusion: str = Field(description="A concluding summary of the research, highlighting key insights and potential risks.")
    
pydantic_report_generator = LlmAgent(
    name="report_generator_agent",
    model="gemini-1.5-pro",
    description="Agent that aggregates inputs from other agents and generates a comprehensive investor report in a structured format.",
    output_schema=Report,
    instruction="""
    You are an AI financial report writer. Your task is to take detailed summaries from a team of expert agents and synthesize them into a single, cohesive, and professional investor report.

    You will receive inputs from the stock data agent and the sentiment analysis agent. Synthesize these inputs into a structured report that follows the schema.

    Use only the information provided in the inputs to fill the `Report` schema. Your goal is to combine the data into a high-quality, readable narrative within each section's summary field. 
    Do not invent or assume any information. Your output must conform exactly to the `Report` schema.
    """,
    output_key="investor_report"
)

report_generator = LlmAgent(
    name="report_generator_agent",
    model="gemini-1.5-pro",
    description="Agent that aggregates inputs from other agents and generates a comprehensive investor report in Markdown format.",
    instruction="""
    You are an AI financial report writer. Your task is to take detailed summaries from the stock data agent 
    and the sentiment analysis agent, then synthesize them into a single, cohesive, and professional investor report.
    You should receive inputs from stock data and sentiment analysis agents. Synthesize these inputs into a structured report.
    Use only the information provided in the inputs to create the report. Do not invent or assume any information.
    If you do not receive information then tell the orchestrator that you are missing information to complete the report.

    The report should always follow this structure in Markdown:

    # {Report Title}

    **Ticker:** {Ticker Symbol}

    ## Fundamentals
    - Narrative summary of valuation and financial health
    - Key metrics (formatted as a bulleted list)
    - Any extra notes

    ## Technicals
    - Narrative summary of recent price action and trends
    - Key indicators (formatted as a bulleted list)
    - Any extra notes

    ## Sentiment
    - Narrative summary of latest news, social media, and analyst sentiment
    - Any extra notes

    ## Conclusion
    - Final summary highlighting key insights and potential risks

    Guidelines:
    - Write in a professional, investor-focused tone.
    - Only use information provided in the inputs. Do not invent facts.
    - Always include all sections, even if some are brief.
    """,
    output_key="investor_report"
)