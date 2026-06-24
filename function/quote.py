import requests

from printer import hr, print_title


def print_quote(printer):
    r = requests.get("http://api.quotable.io/random", timeout=10)

    data = r.json()
    quote = data["content"]
    author = data["author"]

    print_title(printer, "QUOTE:")
    hr(printer)
    printer.text(f"{quote} \n- {author}\n")
    hr(printer)
