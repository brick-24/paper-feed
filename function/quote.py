"""Random inspirational quote from quotable.io."""

from __future__ import annotations

from function.http_client import get_json
from printer import hr, print_title


def print_quote(printer) -> None:
    """Print a random quote."""
    data = get_json("http://api.quotable.io/random", timeout=(5, 10))
    quote = data["content"]
    author = data["author"]

    print_title(printer, "QUOTE:")
    hr(printer)
    printer.text(f"{quote} \n")
    printer.set(align="center", bold=False, width=1, height=1)
    printer.text(f"- {author}\n")
    printer.ln()