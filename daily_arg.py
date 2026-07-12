import argparse

from config import DEFAULT_PRODUCT_ID, DEFAULT_VENDOR_ID
from config import DEFAULT_OPTIONS
from function.comic import print_xkcd
from function.markets import print_markets
from function.news import print_news
from function.quote import print_quote
from function.weather import print_weather
from function.text_inp import print_text_input
from function.image_inp import print_image_input
from function.stock import print_stock
from function.forecast import print_weekly_weather
from printer import TerminalPrinter, create_printer, hr


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
        "--text",
        type=str,
        help="Text to print",
    )

    parser.add_argument(
        "--image",
        type=str,
        help="--text='img path str'",
    )


    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a simple printer test",
    )
    
    #Parse for Stock.py
    parser.add_argument(
        "--stock",
        type=str,
        help="Ticker symbol to look up(e.g. --stock AAPL)"
    )

    parser.add_argument(
        "--forecast",
        action="store_true",
        help="weather forecast"
    )

    parser.add_argument(
        "--news",
        action="store_true",
        help="Print RSS news headlines"
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
        args.quote,
        args.text,
        args.image,
        args.stock,
        args.forecast,
        args.news
    ]):

        for option in DEFAULT_OPTIONS:
            setattr(args, option, True)

    if args.text is not None:
        print_text_input(printer, args.text)

    if args.image is not None:
        print_image_input(printer, args.image)

    if args.weather:
        print_weather(printer, args.city)

    if args.forecast:
        print_weekly_weather(printer, args.city)

    if args.xkcd:
        print_xkcd(printer)

    if args.quote:
        print_quote(printer)

    if args.markets:
        print_markets(printer)

    if args.news:
        print_news(printer)

    if args.stock is not None:
        print_stock(printer, args.stock)


    
    hr(printer)


if __name__ == "__main__":
    main()
