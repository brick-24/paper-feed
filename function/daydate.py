from datetime import datetime
from printer import hr, print_title

def print_daydate(printer):
    now = datetime.now()
    printstr = now.strftime("%A, %d/%m/%Y")
    print_title(printer, printstr)
    hr(printer)
    printer.ln()