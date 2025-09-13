from pydantic import BaseModel, Field
from typing import Optional, List

class ScreeningCriteria(BaseModel):
    """
    A structured schema for stock screening criteria derived from natural language.
    All fields are optional, as the user may not specify every criterion.
    """
    sectors: Optional[List[str]] = Field(
        None,
        description="A list of stock sectors to filter by (e.g., 'Technology', 'Healthcare')."
    )
    market_cap_min_usd: Optional[float] = Field(
        None,
        description="The minimum market capitalization in USD to filter by."
    )
    market_cap_max_usd: Optional[float] = Field(
        None,
        description="The maximum market capitalization in USD to filter by."
    )
    pe_ratio_max: Optional[float] = Field(
        None,
        description="The maximum Price-to-Earnings (P/E) ratio for finding undervalued stocks."
    )
    positive_earnings_growth: Optional[bool] = Field(
        None,
        description="True if the user is looking for stocks with positive earnings growth."
    )
    positive_revenue_growth: Optional[bool] = Field(
        None,
        description="True if the user is looking for stocks with positive revenue growth."
    )
    # Add other criteria as needed (e.g., dividend_yield_min, analyst_rating)


class ScreeningStatus(BaseModel):
    """
    Schema for the final output of the NLP screener agent.
    This provides clear communication to the orchestrator about the success of the translation.
    """
    success: bool = Field(
        ...,
        description="True if the agent successfully identified screening criteria. False if the query was not understood or out of scope."
    )
    criteria: Optional[ScreeningCriteria] = Field(
        None,
        description="The structured screening criteria object. Will be null if success is false."
    )
    error_message: Optional[str] = Field(
        None,
        description="A user-friendly message explaining why the query could not be processed. Will be null if success is true."
    )