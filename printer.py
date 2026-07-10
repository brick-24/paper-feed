from escpos.printer import Usb


def create_printer(vendor_id, product_id):
    return Usb(
        vendor_id,
        product_id,
        in_ep=0x82,
        out_ep=0x04,
    )


class TerminalPrinter:
    WIDTH = 32

    def __init__(self):
        self.align = "left"

    def set(self, **kwargs):
        if "align" in kwargs:
            self.align = kwargs["align"]

    def text(self, text):
        for line in text.splitlines(True):  #'\n'
            if line.endswith("\n"):
                content = line[:-1]
                newline = "\n"
            else:
                content = line
                newline = ""

            if self.align == "center":
                print(f"{content:^{self.WIDTH}}", end=newline)
            else:
                print(content, end=newline)

    def image(self, image_path):
        print(f"[IMAGE: {image_path}]")

    def ln(self):
        print()

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
