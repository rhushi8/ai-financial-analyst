"""Stock price and fundamentals tools using yfinance."""

import logging
import re
from datetime import datetime

import pandas as pd
import yfinance as yf

from finance_ai.schemas.tools import (
    FundamentalsResponse,
    StockPriceResponse,
    StockPricePoint,
)
from finance_ai.utils.cache import cached

logger = logging.getLogger(__name__)
VALID_TICKER = re.compile(r"^\^?[A-Z]{1,10}(?:\.(?:NS|BO|L|HK|T|SI))?$", re.IGNORECASE)


def _is_valid_ticker(ticker: str) -> bool:
    if not ticker:
        return False
    return bool(VALID_TICKER.match(ticker))


def _normalize_history_frame(hist: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Return a single-ticker OHLCV frame with flat columns."""

    if isinstance(hist.columns, pd.MultiIndex):
        if ticker in hist.columns.get_level_values(-1):
            return hist.xs(ticker, axis=1, level=-1, drop_level=True)
        # Fallback: choose first available ticker slice.
        first_symbol = hist.columns.get_level_values(-1)[0]
        return hist.xs(first_symbol, axis=1, level=-1, drop_level=True)
    return hist


@cached(ttl_seconds=300)
def get_stock_price(ticker: str, period: str = "1mo") -> StockPriceResponse:
    """
    Fetch stock price data for a given ticker and period.

    Args:
        ticker: Stock ticker symbol (e.g., AAPL)
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

    Returns:
        StockPriceResponse with current price, change, and historical data
    """
    try:
        ticker = ticker.upper().strip()
        if not _is_valid_ticker(ticker):
            return StockPriceResponse(
                ticker=ticker,
                period=period,
                current_price=0,
                change_pct=0,
                change_abs=0,
                period_high=0,
                period_low=0,
                volume_avg=0,
                retrieved_at=datetime.now(),
                error=f"Invalid ticker format: {ticker}",
            )

        # Fetch historical data
        hist = yf.download(ticker, period=period, progress=False)

        if hist is None or hist.empty:
            return StockPriceResponse(
                ticker=ticker,
                period=period,
                current_price=0,
                change_pct=0,
                change_abs=0,
                period_high=0,
                period_low=0,
                volume_avg=0,
                retrieved_at=datetime.now(),
                error=f"No data found for {ticker}",
            )

        hist = _normalize_history_frame(hist, ticker)

        # Get current price (last close) and period baseline (first open)
        current_price = float(hist["Close"].iloc[-1])
        period_open = float(hist["Open"].iloc[0])
        high_col = hist["High"]
        low_col = hist["Low"]
        vol_col = hist["Volume"]
        change_abs = current_price - period_open
        change_pct = (change_abs / period_open * 100) if period_open != 0 else 0

        # Calculate period high/low and average volume
        period_high = float(high_col.max())
        period_low = float(low_col.min())
        volume_avg = float(vol_col.mean())

        # Build data points
        data_points = []
        for idx in range(len(hist)):
            row_date = hist.index[idx]
            data_points.append(
                StockPricePoint(
                    date=row_date,
                    open=float(hist["Open"].iloc[idx]),
                    high=float(high_col.iloc[idx]),
                    low=float(low_col.iloc[idx]),
                    close=float(hist["Close"].iloc[idx]),
                    volume=int(vol_col.iloc[idx]),
                )
            )

        return StockPriceResponse(
            ticker=ticker,
            period=period,
            current_price=current_price,
            change_pct=round(change_pct, 2),
            change_abs=round(change_abs, 2),
            period_high=round(period_high, 2),
            period_low=round(period_low, 2),
            volume_avg=round(volume_avg, 0),
            data_points=data_points,
            retrieved_at=datetime.now(),
        )

    except Exception as e:
        logger.error("Error fetching stock price for %s: %s", ticker, e)
        return StockPriceResponse(
            ticker=ticker,
            period=period,
            current_price=0,
            change_pct=0,
            change_abs=0,
            period_high=0,
            period_low=0,
            volume_avg=0,
            retrieved_at=datetime.now(),
            error=str(e),
        )


@cached(ttl_seconds=300)
def get_fundamentals(ticker: str) -> FundamentalsResponse:
    """
    Fetch company fundamentals for a given ticker.

    Args:
        ticker: Stock ticker symbol

    Returns:
        FundamentalsResponse with PE ratio, market cap, dividends, etc.
    """
    try:
        ticker = ticker.upper().strip()
        if not _is_valid_ticker(ticker):
            return FundamentalsResponse(
                ticker=ticker,
                retrieved_at=datetime.now(),
                error=f"Invalid ticker format: {ticker}",
            )

        # Fetch ticker info
        yf_ticker = yf.Ticker(ticker)
        info = yf_ticker.info

        return FundamentalsResponse(
            ticker=ticker,
            company_name=info.get("longName"),
            sector=info.get("sector"),
            market_cap=info.get("marketCap"),
            pe_ratio=info.get("trailingPE"),
            dividend_yield=info.get("dividendYield"),
            fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
            fifty_two_week_low=info.get("fiftyTwoWeekLow"),
            avg_volume=info.get("averageVolume"),
            beta=info.get("beta"),
            retrieved_at=datetime.now(),
        )

    except Exception as e:
        logger.error("Error fetching fundamentals for %s: %s", ticker, e)
        return FundamentalsResponse(
            ticker=ticker,
            retrieved_at=datetime.now(),
            error=str(e),
        )
