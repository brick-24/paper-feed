```
████   ███  ████  █████ ████       █████ █████ █████ ████
█   █ █   █ █   █ █     █   █      █     █     █     █   █
████  █████ ████  ████  ████  ████ ████  ████  ████  █   █
█     █   █ █     █     █  █       █     █     █     █   █
█     █   █ █     █████ █   █      █     █████ █████ ████
```

A personal thermal newspaper that automatically generates a daily briefing

Paper-feed has useful modules such as the weather, market metrics, quotes, XKCD comics, stock summaries, etc. which print directly to a USB ESC/POS thermal printer. It can also print arbitrary text and images, making it a lightweight dashboard on paper.

## Features

- Weather forecast for any city (powered by wttr.in)
- Market performance summary
- Individual stock lookup
- Random inspirational quotes
- Latest XKCD comic
- Print custom text
- Print local images
- Terminal test mode (no printer required)

## Requirements

- Python 3.13+
- USB ESC/POS thermal printer (or use `--test` mode for terminal output)

## Installation

Clone the repository:

git clone https://github.com/brick-24/paper-feed.git
cd paper-feed

Install dependencies:

pip install -r requirements.txt

## Printer Configuration

Update the USB Vendor ID and Product ID in config.py:

DEFAULT_VENDOR_ID = 0x0483
DEFAULT_PRODUCT_ID = 0x5840

These values must match your printer.

## Usage

Run with no arguments to print the default feed:

python daily_arg.py

By default, this prints:

- Weather
- Market summary
- Quote

### Print Weather

```python
python daily_arg.py --weather
```

Specify a city:

```python
python daily_arg.py --weather --city Delhi
```

### Print Market Summary

```python
python daily_arg.py --markets
```

### Print Stock Information

```python
python daily_arg.py --stock AAPL
```

or

```python
python daily_arg.py --stock RELIANCE.NS
```

Displays:

- Weekly return
- Monthly return
- Yearly return
- Market capitalization
- P/E ratio
- Dividend yield
- 52-week high/low

### Print a Quote

```python
python daily_arg.py --quote
```

### Print the Latest XKCD

```python
python daily_arg.py --xkcd
```

### Print Custom Text

```python
python daily_arg.py --text "Hello, World!"
```

### Print an Image

```python
python daily_arg.py --image path/to/image.png
```

### Print a QR Code

```python
python daily_arg.py --qrcode "https://example.com"
```

### Test Without a Printer

Print everything to the terminal instead of a USB printer:

```python
python daily_arg.py --test
```

This is useful for development and debugging

## Future Ideas

- Calendar integration
- Todo list printing
- GitHub notifications
- Daily schedule
- Custom templates
- Automatic scheduled printing

If you have any ideas please create issues with the prefix "feature: ..."
