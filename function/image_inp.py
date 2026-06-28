from printer import hr, print_title
from pathlib import Path

def print_image_input(printer, image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    hr(printer)
    printer.image(image_path, center=True)
    hr(printer)
    printer.ln()
