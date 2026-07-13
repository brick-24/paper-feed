import argparse
from collections import OrderedDict

from config import DEFAULT_PRODUCT_ID, DEFAULT_VENDOR_ID
from config import DEFAULT_OPTIONS
from function.comic import print_xkcd
from function.markets import print_markets
from function.quote import print_quote
from function.weather import print_weather
from function.text_inp import print_text_input
from function.image_inp import print_image_input
from function.stock import print_stock
from function.forecast import print_weekly_weather
from printer import TerminalPrinter, create_printer, hr


# Map CLI option name -> (handler_fn, arg_getter, is_flag)
# arg_getter(args) returns the argument value to pass to handler
# is_flag=True means it's a store_true flag (check args.<opt> for truthiness)
OPTION_HANDLERS = OrderedDict([
    ("text", (print_text_input, lambda a: a.text, False)),
    ("image", (print_image_input, lambda a: a.image, False)),
    ("weather", (print_weather, lambda a: a.city, True)),
    ("forecast", (print_weekly_weather, lambda a: a.city, True)),
    ("xkcd", (print_xkcd, lambda a: None, True)),
    ("quote", (print_quote, lambda a: None, True)),
    ("markets", (print_markets, lambda a: None, True)),
    ("stock", (print_stock, lambda a: a.stock, False)),
])

# Default execution order: DEFAULT_OPTIONS first, then remaining handlers
DEFAULT_ORDER = list(DEFAULT_OPTIONS) + [
    opt for opt in OPTION_HANDLERS if opt not in DEFAULT_OPTIONS
]


def parse_args():
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
        help="City for weather/forecast (default: Delhi)",
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Custom text to print",
    )

    parser.add_argument(
        "--image",
        type=str,
        help="Image file path to print",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode (terminal output only)",
    )

    parser.add_argument(
        "--stock",
        type=str,
        help="Ticker symbol to look up (e.g. --stock AAPL)",
    )

    parser.add_argument(
        "--forecast",
        action="store_true",
        help="Print 7-day weather forecast",
    )

    return parser.parse_args()


def _is_option_enabled(args, opt):
    """Check if an option is explicitly enabled by user."""
    handler, arg_getter, is_flag = OPTION_HANDLERS[opt]
    if is_flag:
        return getattr(args, opt) is True
    # For value arguments, enabled if value is provided (not None/empty)
    val = arg_getter(args)
    return val is not None and val != ""


def _get_active_options(args):
    """Return list of enabled option names in DEFAULT_ORDER."""
    return [opt for opt in DEFAULT_ORDER if _is_option_enabled(args, opt)]


def main():
    args = parse_args()

    printer = TerminalPrinter() if args.test else create_printer(
        DEFAULT_VENDOR_ID, DEFAULT_PRODUCT_ID
    )

    # If no explicit flags, enable DEFAULT_OPTIONS
    if not _get_active_options(args):
        for opt in DEFAULT_OPTIONS:
            setattr(args, opt, True)

    # Execute handlers in configured order
    for opt in _get_active_options(args):
        handler, arg_getter, is_flag = OPTION_HANDLERS[opt]
        if is_flag:
            handler(printer)
        else:
            arg_val = arg_getter(args)
            if arg_val:
                handler(printer, arg_val)

    hr(printer)


if __name__ == "__main__":
    main()