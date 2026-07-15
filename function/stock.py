"""Individual stock lookup with financial details."""

from __future__ import annotations

from function.market_calc import calculate_returns, format_market_cap, get_financials
from printer import hr, print_title


def print_stock(printer, ticker: str) -> None:
    """Print detailed stock information."""
    print_title(printer, f"{ticker.upper()}:")
    hr(printer)

    try:
        returns = calculate_returns(ticker, period="1y", intervals=("week", "month", "year"))
        fin = get_financials(ticker)
    except Exception:
        printer.text("Could not fetch data for this ticker\n")
        printer.ln()
        return

    week = returns.get("week")
    month = returns.get("month")
    year = returns.get("year")

    printer.text(
        f"Week: {week:+.1f}%  "
        f"Month: {month:+.1f}%  "
        f"Year: {year:+.1f}%\n"
    )
    printer.text(f"Market Cap: {format_market_cap(fin['market_cap'])}\n")
    printer.text(f"P/E Ratio:  {fin['pe_ratio'] if fin['pe_ratio'] else 'N/A'}\n")

    if fin["dividend_yield"]:
        printer.text(f"Div yield: {fin['dividend_yield']:.2f}%\n")

    printer.text(f"52wk High: {fin['high_52wk']}\n")
    printer.text(f"52wk Low: {fin['low_52wk']}\n")

    printer.ln()