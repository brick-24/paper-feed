"""Shared market calculations for markets and stock modules."""

from __future__ import annotations

from typing import Any

import yfinance as yf


def calculate_returns(
    ticker: str,
    period: str = "1y",
    intervals: tuple[str, ...] = ("day", "week", "month", "year"),
) -> dict[str, float | None]:
    """Calculate returns for a ticker over multiple periods.

    Args:
        ticker: Yahoo Finance ticker symbol.
        period: History period to fetch (e.g., "1y", "2mo", "5y").
        intervals: Which periods to calculate. Options: "day", "week", "month", "year".

    Returns:
        Dict with keys from intervals, values are percentage returns (or None if insufficient data).
    """
    hist = yf.Ticker(ticker).history(period=period)
    closes = hist["Close"].dropna()

    if len(closes) < 2:
        return {k: None for k in intervals}

    current = closes.iloc[-1]
    returns: dict[str, float | None] = {}

    if "day" in intervals and len(closes) >= 2:
        returns["day"] = ((current - closes.iloc[-2]) / closes.iloc[-2]) * 100
    else:
        returns["day"] = None

    if "week" in intervals and len(closes) >= 6:
        returns["week"] = ((current - closes.iloc[-6]) / closes.iloc[-6]) * 100
    else:
        returns["week"] = None

    if "month" in intervals and len(closes) >= 22:
        returns["month"] = ((current - closes.iloc[-22]) / closes.iloc[-22]) * 100
    else:
        returns["month"] = None

    if "year" in intervals:
        if len(closes) >= 252:
            returns["year"] = ((current - closes.iloc[-252]) / closes.iloc[-252]) * 100
        elif len(closes) > 1:
            returns["year"] = ((current - closes.iloc[0]) / closes.iloc[0]) * 100
        else:
            returns["year"] = None

    return returns


def get_financials(ticker: str) -> dict[str, Any]:
    """Fetch key financial metrics for a ticker.

    Returns:
        Dict with: market_cap, pe_ratio, dividend_yield, high_52wk, low_52wk.
    """
    info = yf.Ticker(ticker).info

    return {
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "dividend_yield": info.get("dividendYield"),
        "high_52wk": info.get("fiftyTwoWeekHigh"),
        "low_52wk": info.get("fiftyTwoWeekLow"),
    }


def format_market_cap(value: float | None) -> str:
    """Format market cap with K/M/B/T suffix."""
    if value is None:
        return "N/A"
    for unit in ("", "K", "M", "B", "T"):
        if abs(value) < 1000:
            return f"{value:.1f}{unit}"
        value /= 1000
    return f"{value:.1f}Q"