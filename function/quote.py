import requests

from printer import hr, print_title


def print_quote(printer):
    r = requests.get("http://api.quotable.io/random", timeout=10)

    data = r.json()
    quote = data["content"]
    author = data["author"]

    print_title(printer, "QUOTE:")
    hr(printer)
    printer.text(f"{quote} \n")
    printer.set(align="center", bold = False, width = 1, height = 1)
    printer.text(f"- {author}\n")
    hr(printer)
