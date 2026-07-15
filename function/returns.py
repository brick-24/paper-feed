"""Market performance calculations (shared between markets and stock modules)."""

from __future__ import annotations

import yfinance as yf


def calculate_returns(ticker: str, period: str = "1y") -> dict[str, float]:
    """Calculate returns for a ticker over various periods.

    Args:
        ticker: Yahoo Finance ticker symbol.
        period: History period to fetch (e.g., '2mo', '1y', '2y').

    Returns:
        Dict with return percentages for available periods.
        Keys may include: 'day', 'week', 'month', 'year'.

    Raises:
        ValueError: If insufficient price history.
    """
    hist = yf.Ticker(ticker).history(period=period)
    closes = hist["Close"].dropna()

    if len(closes) < 2:
        raise ValueError("Not enough history")

    current = closes.iloc[-1]
    returns = {}

    # Day-over-day (need at least 2 days)
    if len(closes) >= 2:
        returns["day"] = ((current - closes.iloc[-2]) / closes.iloc[-2]) * 100

    # Week (approx 5 trading days)
    if len(closes) >= 6:
        returns["week"] = ((current - closes.iloc[-6]) / closes.iloc[-6]) * 100

    # Month (approx 21 trading days)
    if len(closes) >= 22:
        returns["month"] = ((current - closes.iloc[-22]) / closes.iloc[-22]) * 100

    # Year (approx 252 trading days)
    if len(closes) >= 252:
        returns["year"] = ((current - closes.iloc[-252]) / closes.iloc[-252]) * 100
    elif len(closes) > 1:
        returns["year"] = ((current - closes.iloc[0]) / closes.iloc[0]) * 100

    return returns