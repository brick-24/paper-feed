from printer import hr, print_title


def print_text_input(printer, text):
    hr(printer)
    printer.text(f"{text} \n")
    hr(printer)
    printer.ln()
