import qrcode
from PIL import Image
from printer import hr, print_title


def print_qr_code(printer, data, version=None, box_size=2, border=2):
    """Print a QR code for the given data as ASCII art.
    
    Args:
        printer: Printer instance
        data: String/URL to encode in the QR code
        version: QR code version (1-40), None for auto
        box_size: Size of each box in pixels
        border: Border size in boxes
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    print_title(printer, "QR CODE:")
    hr(printer)

    # Print QR code as ASCII art
    matrix = img.convert("1").load()
    width, height = img.size

    printer.set(align="center", bold=False, width=1, height=1)
    for y in range(height):
        line = ""
        for x in range(width):
            line += "\u2588\u2588" if matrix[x, y] == 0 else "  "
        printer.text(line + "\n")
    printer.ln()


def print_qr_code_image(printer, data, version=None, box_size=10, border=4):
    """Print a QR code as an image (for actual thermal printers).
    
    Args:
        printer: Printer instance with image printing capability
        data: String/URL to encode in the QR code
        version: QR code version (1-40), None for auto
        box_size: Size of each box in pixels
        border: Border size in boxes
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    print_title(printer, "QR CODE:")
    hr(printer)
    
    # Print as image - requires printer with image support
    printer.image(img)
    printer.ln()