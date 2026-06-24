import tempfile
from pathlib import Path

import requests
from PIL import Image

from printer import hr, print_title


def download_xkcd():
    r = requests.get(
        "https://xkcd.com/info.0.json",
        timeout=10,
    )
    r.raise_for_status()

    data = r.json()

    img = requests.get(
        data["img"],
        timeout=20,
    )
    img.raise_for_status()

    with tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False,
    ) as f:
        f.write(img.content)
        path = Path(f.name)

    image = Image.open(path)
    image.convert("L").save(path)

    return {
        "title": data["safe_title"],
        "num": data["num"],
        "image_path": path,
    }


def print_xkcd(printer):
    comic = download_xkcd()

    print_title(printer, "XKCD:")
    hr(printer)

    printer.set(
        align="center",
        bold=False,
        width=1,
        height=1,
    )

    printer.text(f"#{comic['num']}\n")
    printer.text(f"{comic['title']}\n\n")

    printer.image(str(comic["image_path"]))
    # hr(printer)
