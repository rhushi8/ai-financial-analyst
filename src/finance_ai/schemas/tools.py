"""Tool input and output schemas for finance analyst."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StockPriceRequest(BaseModel):
    """Input schema for stock price lookup."""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT)")
    period: str = Field(
        default="1mo", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
    )


class StockPricePoint(BaseModel):
    """Single price data point."""

    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class StockPriceResponse(BaseModel):
    """Output schema for stock price data."""

    ticker: str
    period: str
    current_price: float
    change_pct: float
    change_abs: float
    period_high: float
    period_low: float
    volume_avg: float
    data_points: Optional[list[StockPricePoint]] = Field(
        default=None, description="Historical OHLCV data if requested"
    )
    retrieved_at: datetime
    error: Optional[str] = None


class FundamentalsRequest(BaseModel):
    """Input schema for company fundamentals."""

    ticker: str = Field(..., description="Stock ticker symbol")


class FundamentalsResponse(BaseModel):
    """Output schema for company fundamentals."""

    ticker: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    avg_volume: Optional[float] = None
    beta: Optional[float] = None
    retrieved_at: datetime
    error: Optional[str] = None


class CalculatorRequest(BaseModel):
    """Input schema for financial calculations."""

    operation: str = Field(
        ...,
        description="Operation type: pct_change, price_target, pe_multiple, dividend_income",
    )
    params: dict = Field(..., description="Parameters for the operation")


class CalculatorResponse(BaseModel):
    """Output schema for calculations."""

    operation: str
    result: float
    formatted_result: str
    details: dict = Field(default_factory=dict)
    retrieved_at: datetime
    error: Optional[str] = None


class NewsArticle(BaseModel):
    """Single news article reference."""

    source: str
    title: str
    url: str
    published_date: Optional[datetime] = None
    summary: Optional[str] = None


class NewsSearchResponse(BaseModel):
    """Output schema for news retrieval."""

    query: str
    articles: list[NewsArticle]
    retrieved_at: datetime
    error: Optional[str] = None


class MarketIdea(BaseModel):
    """Single market idea candidate for India-focused screening."""

    ticker: str
    company_name: str
    action: str
    score: float
    rationale: str
    change_pct_1m: Optional[float] = None
    sector: Optional[str] = None
    index_membership: list[str] = Field(default_factory=list)


class IndiaMarketIdeasResponse(BaseModel):
    """Output schema for India market ideas generation."""

    query: str
    market_snapshot: dict = Field(default_factory=dict)
    ideas: list[MarketIdea] = Field(default_factory=list)
    disclaimer: str = (
        "Educational output only, not investment advice. Verify with risk profile and independent research."
    )
    retrieved_at: datetime
    error: Optional[str] = None


class ToolTrace(BaseModel):
    """Record of a tool execution for transparency."""

    tool_name: str
    input_params: dict
    output: dict
    duration_ms: float
    success: bool
    error: Optional[str] = None
