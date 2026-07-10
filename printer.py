from escpos.printer import Usb


def create_printer(vendor_id, product_id):
    return Usb(
        vendor_id,
        product_id,
        in_ep=0x82,
        out_ep=0x04,
    )


class TerminalPrinter:
    def set(self, **kwargs):
        return

    def text(self, text):
        print(text, end="")

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
