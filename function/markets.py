import yfinance as yf

from config import TICKERS
from printer import hr, print_title


def calculate_returns(ticker):
    hist = yf.Ticker(ticker).history(period="2mo")

    closes = hist["Close"].dropna()

    if len(closes) < 22:
        raise ValueError("Not enough history")

    current = closes.iloc[-1]

    return {
        "day": ((current - closes.iloc[-2]) / closes.iloc[-2]) * 100,
        "week": ((current - closes.iloc[-6]) / closes.iloc[-6]) * 100,
        "month": ((current - closes.iloc[-22]) / closes.iloc[-22]) * 100,
    }


def print_markets(printer):
    print_title(printer, "MARKETS:")

    hr(printer)

    rows = []

    for name, ticker in TICKERS.items():
        try:
            perf = calculate_returns(ticker)

            rows.append({
                "name": name,
                "day": perf["day"],
                "week": perf["week"],
                "month": perf["month"],
            })

        except Exception:
            rows.append({
                "name": name,
                "day": float("-inf"),
                "week": None,
                "month": None,
            })

    rows.sort(key=lambda x: x["day"], reverse=True)

    printer.text("Stock Day:\tWeek:\tMonth:\n")

    for row in rows:
        if row["week"] is None:
            printer.text(f"{row['name']:<5} ERR\n")
            continue

        printer.text(
            f"{row['name']:<5} "
            f"{row['day']:+.1f}%\t"
            f"{row['week']:+.1f}%\t"
            f"{row['month']:+.1f}%\n"
        )

    # hr(printer)
