import os

import yfinance as yf
import matplotlib.pyplot as plt
from function.image_inp import print_image_input

def print_stock_performance(printer, ticker, period="1mo"):
    data = yf.Ticker(ticker).history(
        period=period,
        auto_adjust=True,
    )

    if data.empty:
        raise ValueError(f"No data found for {ticker}")

    os.makedirs("img", exist_ok=True)

    filename = f"img/{ticker.lower()}.png"

    plt.figure(figsize=(10, 5))

    plt.plot(
        data.index,
        data["Close"],
        linewidth=2,
    )

    plt.title(f"{ticker.upper()} Stock Performance")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()