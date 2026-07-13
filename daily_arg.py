import argparse
from collections import OrderedDict
from typing import Callable, Optional

from config import DEFAULT_OPTIONS, DEFAULT_PRODUCT_ID, DEFAULT_VENDOR_ID
from function.comic import print_xkcd
from function.forecast import print_weekly_weather
from function.image_inp import print_image_input
from function.markets import print_markets
from function.quote import print_quote
from function.stock import print_stock
from function.text_inp import print_text_input
from function.weather import print_weather
from printer import TerminalPrinter, create_printer, hr


HandlerFn = Callable[..., None]
ArgGetter = Callable[[argparse.Namespace], Optional[str]]

OPTION_HANDLERS: "OrderedDict[str, tuple[HandlerFn, ArgGetter]]" = OrderedDict(
    [
        ("weather", (print_weather, lambda a: a.city)),
        ("forecast", (print_weekly_weather, lambda a: a.city)),
        ("markets", (print_markets, lambda a: None)),
        ("quote", (print_quote, lambda a: None)),
        ("xkcd", (print_xkcd, lambda a: None)),
        ("text", (print_text_input, lambda a: a.text)),
        ("image", (print_image_input, lambda a: a.image)),
        ("stock", (print_stock, lambda a: a.stock)),
    ]
)

DEFAULT_ORDER = list(DEFAULT_OPTIONS) + [opt for opt in OPTION_HANDLERS if opt not in DEFAULT_OPTIONS]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--quote",
        action="store_true",
        help="Print a random quote",
    )

    parser.add_argument(
        "--xkcd",
        action="store_true",
        help="Print latest XKCD comic",
    )

    parser.add_argument(
        "--weather",
        action="store_true",
        help="Print current weather",
    )

    parser.add_argument(
        "--markets",
        action="store_true",
        help="Print market summary",
    )

    parser.add_argument(
        "--city",
        default="Delhi",
        help="Weather city (default: Delhi)",
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Custom text to print",
    )

    parser.add_argument(
        "--image",
        type=str,
        help="Path to image file to print",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode (terminal output only)",
    )

    parser.add_argument(
        "--stock",
        type=str,
        help="Ticker symbol to look up (e.g., AAPL)",
    )

    parser.add_argument(
        "--forecast",
        action="store_true",
        help="Print 7-day weather forecast",
    )

    return parser.parse_args()


def _get_active_options(args: argparse.Namespace) -> list[str]:
    """Return active option names in execution order."""
    explicit = [opt for opt in DEFAULT_ORDER if getattr(args, opt, None)]
    if explicit:
        return explicit
    return list(DEFAULT_OPTIONS)


def main() -> None:
    args = parse_args()

    printer = TerminalPrinter() if args.test else create_printer(
        DEFAULT_VENDOR_ID, DEFAULT_PRODUCT_ID
    )

    for opt_name in _get_active_options(args):
        handler, arg_getter = OPTION_HANDLERS[opt_name]
        arg = arg_getter(args)
        if arg is not None:
            handler(printer, arg)
        else:
            handler(printer)

    hr(printer)


if __name__ == "__main__":
    main()