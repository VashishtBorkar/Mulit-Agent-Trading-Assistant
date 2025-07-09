from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent

class StockInformation(BaseModel):
    ticker: str
    current_price: float
    rsi: float
    sentiment_summary: str
    valuation_summary: str
    recommendation: str | None # Empty for the strategy agent

output_agent = LlmAgent(
    name="output_agent",
    model="gemini-1.5-pro",  # required because this agent generates output
    description="Agent that converts multi-agent responses into structured output.",
    output_schema=StockInformation,
    instruction="""
    You are an AI responsible for converting agent outputs into a structured stock analysis object.

    You will receive the following input summaries from earlier agents:

    * **Market Data:**
    {market_agent_result}

    * **Sentiment Analysis:**
    {sentiment_agent_result}

    * **Fundamental Analysis:**
    {fundamentals_agent_result}

    Use only the information provided above to fill the `StockInformation` schema:
    - Extract the `ticker` (e.g., AAPL, TSLA).
    - From the market data, extract the current stock price and RSI.
    - From the sentiment data, summarize sentiment in a descriptive paragraph.
    - From the fundamental data, summarize key valuation or financial points.
    - Leave the `recommendation` field blank (null); it will be filled by the strategy agent.

    Do not invent or assume any information not explicitly found in the inputs. Your output must conform exactly to the `StockInformation` schema.
    """,
    output_key="stock_information_result"
)