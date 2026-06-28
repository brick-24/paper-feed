import argparse

from config import DEFAULT_PRODUCT_ID, DEFAULT_VENDOR_ID
from function.comic import print_xkcd
from function.markets import print_markets
from function.quote import print_quote
from function.weather import print_weather
from function.text_inp import print_text_input
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
        default="Enter Text",
        help="--text='text to print'",
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
        args.quote,
        args.text
    ]):
        args.xkcd = True
        args.weather = True
        args.markets = True
        args.quote = True

    if args.text:
        print_text_input(printer, args.text)

    if args.weather:
        print_weather(printer, args.city)

    if args.xkcd:
        print_xkcd(printer)

    if args.quote:
        print_quote(printer)

    if args.markets:
        print_markets(printer)

    
    hr(printer)


if __name__ == "__main__":
    main()
