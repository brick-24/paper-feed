"""XKCD comic fetcher and printer."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from function.http_client import get_content, get_json
from PIL import Image
from printer import hr, print_title


def download_xkcd() -> dict[str, Any]:
    """Download latest XKCD comic and convert to grayscale.

    Returns:
        Dict with keys: title, num, image_path (Path to temp file).
    """
    data = get_json("https://xkcd.com/info.0.json", timeout=(5, 10))

    img_content = get_content(data["img"], timeout=(5, 20))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(img_content)
        path = Path(f.name)

    image = Image.open(path)
    image.convert("L").save(path)

    return {
        "title": data["safe_title"],
        "num": data["num"],
        "image_path": path,
    }


def print_xkcd(printer) -> None:
    """Print latest XKCD comic."""
    comic = download_xkcd()

    print_title(printer, "XKCD:")
    hr(printer)

    printer.set(align="center", bold=False, width=1, height=1)

    printer.text(f"#{comic['num']}\n")
    printer.text(f"{comic['title']}\n\n")

    printer.image(str(comic["image_path"]), center=True)
    printer.ln()