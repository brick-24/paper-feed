"""Market summary table using shared calculations."""

from __future__ import annotations

from config import TICKERS
from function.market_calc import calculate_returns
from printer import hr, print_title


def print_markets(printer) -> None:
    """Print market summary table."""
    print_title(printer, "MARKETS:")
    hr(printer)

    rows = []

    for name, ticker in TICKERS.items():
        try:
            perf = calculate_returns(ticker, period="2mo", intervals=("day", "week", "month"))
            rows.append({
                "name": name,
                "day": perf.get("day"),
                "week": perf.get("week"),
                "month": perf.get("month"),
            })
        except Exception:
            rows.append({
                "name": name,
                "day": float("-inf"),
                "week": None,
                "month": None,
            })

    # Sort by day return (errors at bottom)
    rows.sort(key=lambda x: x["day"] if x["day"] != float("-inf") else float("-inf"), reverse=True)

    printer.text("Stock Day:\tWeek:\tMonth:\n")

    for row in rows:
        if row["week"] is None:
            printer.text(f"{row['name']:<5} ERR\n")
            continue

        day = f"{row['day']:+.1f}%" if row["day"] is not None else "N/A"
        week = f"{row['week']:+.1f}%"
        month = f"{row['month']:+.1f}%"

        printer.text(
            f"{row['name']:<5} "
            f"{day}\t"
            f"{week}\t"
            f"{month}\n"
        )

    printer.ln()