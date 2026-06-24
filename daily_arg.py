import argparse
import tempfile
from pathlib import Path

import requests
import yfinance as yf
from escpos.printer import Usb
from PIL import Image

DEFAULT_VENDOR_ID = 0x0483
DEFAULT_PRODUCT_ID = 0x5840

TICKERS = {
    "NIFTY": "^NSEI",
    "SENSX": "^BSESN",
    "BANK": "^NSEBANK",
    "N50": "NIFTYBEES.NS",
    "BANK": "BANKBEES.NS",
    "IT": "ITBEES.NS",
    "PHAR": "PHARMABEES.NS",
    "AUTO": "AUTOBEES.NS",
    "CPSE": "CPSEETF.NS",
    "PSUB": "PSUBNKBEES.NS",
    "INFR": "INFRABEES.NS",
    "GOLD": "GOLDBEES.NS",
    "HANG": "HNGSNGBEES.NS",

    # "ITC": "ITC.NS",
    # "JUB": "JUBLFOOD.NS",
    # "JKP": "JKPAPER.NS",
    # "JAI": "JISLJALEQS.NS",
    # "HNG": "HNGSNGBEES.NS",

    # "N50": "NIFTYBEES.NS",
    # "PVR": "PVRINOX.NS",
    # "APLH": "APOLLOHOSP.NS",
    # "APLT": "APOLLOTYRE.NS",
    # "BATA": "BATAINDIA.NS",
    # "RIL": "RELIANCE.NS",
    # "RAY": "RAYMOND.NS",
    # "ITCH": "ITCHOTELS.NS",
    # "NEST": "NESTLEIND.NS",
    # "PAY": "PAYTM.NS",
    # "FORT": "FORTIS.NS",
    # "PFZ": "PFIZER.NS",
    # "CIP": "CIPLA.NS",
    # "IRCT": "IRCTC.NS",
    # "TCS": "TCS.NS",
    # "INFY": "INFY.NS",
    # "TSTL": "TATASTEEL.NS",
    # "GOLD": "GOLDBEES.NS",
    # "IOC": "IOC.NS",
    # "MAX": "MAXHEALTH.NS",
    # "JIOFN": "JIOFIN.NS",
    # "MOTR": "TMCV.NS",
    # "OIL": "OIL.NS",

}

def create_printer(vendor_id, product_id):
    return Usb(
        vendor_id,
        product_id,
        in_ep=0x82,
        out_ep=0x04,
    )


class TerminalPrinter:
    def set(self, **kwargs):
        return

    def text(self, text):
        print(text, end="")

    def image(self, image_path):
        print(f"[IMAGE: {image_path}]")


def print_title(printer, title):
    printer.set(
        align="center",
        bold=True,
        width=2,
        height=2,
    )
    printer.text(f"{title}\n")

    printer.set(
        align="left",
        bold=False,
        width=1,
        height=1,
    )


def hr(printer):
    printer.text("--------------------------------\n")

def download_xkcd():
    r = requests.get(
        "https://xkcd.com/info.0.json",
        timeout=10,
    )
    r.raise_for_status()

    data = r.json()

    img = requests.get(
        data["img"],
        timeout=20,
    )
    img.raise_for_status()

    with tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False,
    ) as f:
        f.write(img.content)
        path = Path(f.name)

    image = Image.open(path)
    image.convert("L").save(path)

    return {
        "title": data["safe_title"],
        "num": data["num"],
        "image_path": path,
    }


def print_xkcd(printer):
    comic = download_xkcd()

    printer.set(
        align="center",
        bold=True,
        width=2,
        height=2,
    )
    printer.text("XKCD\n")

    printer.set(
        align="center",
        bold=False,
        width=1,
        height=1,
    )

    printer.text(f"#{comic['num']}\n")
    printer.text(f"{comic['title']}\n\n")

    printer.image(str(comic["image_path"]))
    printer.text("\n")

def get_weather(city):
    r = requests.get(
        f"https://wttr.in/{city}",
        params={"format": "j1"},
        timeout=10,
    )
    r.raise_for_status()

    current = r.json()["current_condition"][0]

    return {
        "description": current["weatherDesc"][0]["value"],
        "temp": current["temp_C"],
        "feels_like": current["FeelsLikeC"],
        "humidity": current["humidity"],
        "precip": current["precipMM"],
    }

def print_quote(printer):
    r = requests.get("http://api.quotable.io/random",timeout=10)

    data = r.json()
    quote = data["content"]
    author = data["author"]

    print_title(printer, "QUOTE:")
    hr(printer)
    printer.text(f"{quote} \n- {author}\n")
    hr(printer)

def print_weather(printer, city):
    weather = get_weather(city)

    print_title(printer, "WEATHER")

    hr(printer)

    printer.text(f"{weather['description']}\n\n")
    printer.text(f"Temp:            {weather['temp']} C\n")
    printer.text(f"Feels Like:      {weather['feels_like']} C\n")
    printer.text(f"Humidity:        {weather['humidity']}%\n")
    printer.text(f"Rain:            {weather['precip']} mm\n")

    hr(printer)

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
    print_title(printer, "MARKETS")

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

    hr(printer)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--quote",
        action="store_true",
        help="what do u think?"
    )

    parser.add_argument(
        "--xkcd",
        action="store_true",
        help="Print latest XKCD",
    )

    parser.add_argument(
        "--weather",
        action="store_true",
        help="Print weather",
    )

    parser.add_argument(
        "--markets",
        action="store_true",
        help="Print market summary",
    )

    parser.add_argument(
        "--city",
        default="Delhi",
        help="Weather city",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a simple printer test",
    )

    return parser.parse_args()

def main():
    args = parse_args()

    printer = TerminalPrinter() if args.test else create_printer(
        DEFAULT_VENDOR_ID, DEFAULT_PRODUCT_ID
    )

    if not any([
        args.xkcd,
        args.weather,
        args.markets,
        args.quote
    ]):
        args.xkcd = True
        args.weather = True
        args.markets = True
        args.quote = True

    if args.weather:
        print_weather(printer, args.city)
    
    if args.xkcd:
        print_xkcd(printer)

    if args.quote:
        print_quote(printer)


    if args.markets:
        print_markets(printer)

    printer.cut()

if __name__ == "__main__":
    main()