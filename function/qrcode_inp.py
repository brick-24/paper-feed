"""QR code generation and printing for thermal printers."""

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image
from printer import hr, print_title


def generate_qr_code(data: str, box_size: int = 2, border: int = 1) -> Image.Image:
    """Generate a QR code image from the given data string.
    
    Args:
        data: The data to encode in the QR code
        box_size: Size of each box in pixels (smaller for thermal printers)
        border: Border size in boxes
    
    Returns:
        PIL Image object containing the QR code
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-determine version
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("1")  # 1-bit mode for thermal printer


def print_qr_code(printer, data: str, box_size: int = 2, border: int = 1, title: str | None = None):
    """Print a QR code to the thermal printer.
    
    Args:
        printer: Printer instance (TerminalPrinter or ESC/POS printer)
        data: Data to encode in the QR code
        box_size: Size of each QR module (default 2 for thermal printers)
        border: Quiet zone border size (default 1)
        title: Optional title to print above the QR code
    """
    if title:
        print_title(printer, title)
    else:
        print_title(printer, "QR CODE:")
    hr(printer)
    
    img = generate_qr_code(data, box_size=box_size, border=border)
    
    # Print image using the printer's image method
    if hasattr(printer, 'image'):
        printer.image(img)
    else:
        # TerminalPrinter fallback - print as ASCII
        _print_qr_ascii(printer, img)
    
    printer.ln()


def _print_qr_ascii(printer, img: Image.Image):
    """Print QR code as ASCII art for terminal testing."""
    width, height = img.size
    pixels = img.load()
    
    for y in range(height):
        line = ""
        for x in range(width):
            line += "██" if pixels[x, y] == 0 else "  "
        printer.text(line + "\n")


def print_qr_code_from_args(printer, data: str, box_size: int = 2):
    """Convenience function for CLI integration."""
    print_qr_code(printer, data, box_size=box_size)