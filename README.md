```
████   ███  ████  █████ ████       █████ █████ █████ ████
█   █ █   █ █   █ █     █   █      █     █     █     █   █
████  █████ ████  ████  ████  ████ ████  ████  ████  █   █
█     █   █ █     █     █  █       █     █     █     █   █
█     █   █ █     █████ █   █      █     █████ █████ ████
```

A personal thermal newspaper that automatically generates a daily briefing and prints it to a USB ESC/POS thermal printer.

Paper-feed includes built-in modules for weather, market metrics, stock lookups, inspirational quotes, XKCD comics, custom text, and image printing. It also runs in a terminal test mode (no printer required) for development and debugging.

---

## Features

- **Weather** — Current conditions + 7-day forecast for any city (powered by Open-Meteo + wttr.in)
- **Markets** — Major index performance (NIFTY, SENSEX, sector ETFs) via yfinance
- **Stocks** — Individual ticker lookup with returns, market cap, P/E, dividend yield, 52-week range
- **Quotes** — Random inspirational quotes from quotable.io
- **XKCD** — Latest comic, downloaded, converted to grayscale, and printed as an image
- **Custom Text** — Print arbitrary text from the command line
- **Images** — Print local image files (auto-converted to 1-bit thermal format)
- **Test Mode** — Full terminal output simulation (no printer required)

---

## Requirements

- **Python 3.11+** (tested on 3.11, 3.12, 3.13)
- **USB ESC/POS thermal printer** (or use `--test` mode for terminal output)
- **Linux / macOS / Windows** (WSL recommended on Windows)
- **Python dependencies** (see [Installation](#installation))

### Hardware Compatibility

| Printer Type           | Connection     | Notes                                                    |
|------------------------|----------------|----------------------------------------------------------|
| USB ESC/POS            | USB            | Most common; uses vendor/product ID                      |
| Bluetooth ESC/POS      | Bluetooth SPP  | Pair first, then use as serial port (`/dev/rfcomm0`)         |
| Serial (RS-232/TTL)    | Serial / USB   | Use `Serial` printer class; configure baud rate          |
| Network (Wi-Fi/Ethernet)| TCP/IP        | Use `Network` printer class; requires IP + port (9100)   |
| Windows Virtual COM    | COM port       | Install printer driver, note COM port number             |

> **Tested printers:** Munbyn ITPP047, MUNBYN ITPP941, Rongta RPP02/03, generic 58mm/80mm USB thermal printers (0x0483/0x5840).

---

## Installation

```bash
# Clone the repository
git clone https://github.com/brick-24/paper-feed.git
cd paper-feed

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies (requirements.txt)

| Package        | Purpose                              |
|----------------|--------------------------------------|
| `escpos`       | ESC/POS printer communication        |
| `yfinance`     | Stock/market data via Yahoo Finance  |
| `requests`     | HTTP calls (weather, quotes, XKCD)   |
| `feedparser`   | RSS feed parsing                     |
| `Pillow`       | Image processing / grayscale convert |
| `python-dateutil` | Date parsing utilities            |
| `pyyaml`       | YAML config support (future)         |

---

## Printer Configuration

### USB Printer (Default)

Edit `config.py` to match your printer's USB IDs:

```python
# config.py
DEFAULT_VENDOR_ID  = 0x0483   # Find with: lsusb
DEFAULT_PRODUCT_ID = 0x5840
```

**Find your printer's IDs:**

```bash
# Linux/macOS
lsusb
# Look for your printer, e.g.:
# Bus 001 Device 012: ID 0483:5840 STMicroelectronics Thermal Printer
# Vendor ID = 0x0483, Product ID = 0x5840
```

```powershell
# Windows (PowerShell)
Get-PnpDevice -Class Printer | Format-Table -AutoSize
# Or use Device Manager -> Properties -> Details -> Hardware Ids
```

### Default Print Modules

```python
# config.py
DEFAULT_OPTIONS = ["weather", "markets", "quote"]
```

Run with no arguments to print the default feed (weather + markets + quote). Override with CLI flags.

### Stock Ticker Configuration

```python
# config.py
TICKERS = {
    "NIFTY": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK": "^NSEBANK",
    # ... add your own tickers here
}
```

---

## Alternative Printer Connections

### Bluetooth (Linux/macOS)

```bash
# 1. Pair and trust the printer
bluetoothctl
# > scan on
# > pair <MAC>
# > trust <MAC>
# > connect <MAC>

# 2. Bind to RFCOMM (creates /dev/rfcomm0)
sudo rfcomm bind 0 <MAC_ADDRESS> 1

# 3. Use Serial printer class in code:
from escpos.printer import Serial
printer = Serial(devfile="/dev/rfcomm0", baudrate=9600)
```

### Network / Wi-Fi Printer (TCP/IP)

```python
from escpos.printer import Network
printer = Network("192.168.1.100", port=9100)
```

### Serial / USB-Serial (RS-232 or USB-to-TTL)

```python
from escpos.printer import Serial
printer = Serial(devfile="/dev/ttyUSB0", baudrate=9600)
# Windows: devfile="COM3"
```

### Windows Setup

1. Install the printer vendor's Windows driver (creates a virtual COM port).
2. Note the COM port number (e.g., `COM3`) from Device Manager.
3. Use the `Serial` printer class with `devfile="COM3"`.
4. For USB direct printing, install [Zadig](https://zadig.akeo.ie/) and replace the driver with **libusbK** or **WinUSB**, then use the USB IDs in `config.py`.

> **Tip:** On Windows, WSL2 + USB passthrough is often more reliable than native USB printing.

---

## Usage

```bash
# Run default feed (weather + markets + quote)
python daily_arg.py

# Test mode — prints to terminal instead of printer
python daily_arg.py --test
```

### Command-Line Options

| Flag | Argument | Description |
|------|----------|-------------|
| `--weather` | — | Print current weather + 7-day forecast |
| `--city` | `<city>` | City for weather (default: `Delhi`) |
| `--forecast` | — | Print 7-day forecast only |
| `--markets` | — | Print market summary table |
| `--stock` | `<TICKER>` | Print stock details (e.g., `AAPL`, `RELIANCE.NS`) |
| `--quote` | — | Print random inspirational quote |
| `--xkcd` | — | Print latest XKCD comic |
| `--text` | `"text"` | Print custom text |
| `--image` | `<path>` | Print local image file (PNG/JPG) |
| `--test` | — | Terminal test mode (no printer) |

### Examples

```bash
# Weather for a specific city
python daily_arg.py --weather --city "New York"

# Market summary only
python daily_arg.py --markets

# Stock lookup (US ticker)
python daily_arg.py --stock AAPL

# Stock lookup (Indian ticker, NSE)
python daily_arg.py --stock RELIANCE.NS

# Just a quote
python daily_arg.py --quote

# Latest XKCD comic
python daily_arg.py --xkcd

# Custom text
python daily_arg.py --text "Hello, thermal world!"

# Print an image
python daily_arg.py --image ./photo.png

# Combine multiple modules
python daily_arg.py --weather --city London --stock TSLA --quote --test
```

### Default Feed Behavior

Running without arguments enables `DEFAULT_OPTIONS` from `config.py`:

```bash
python daily_arg.py
# Equivalent to:
python daily_arg.py --weather --markets --quote
```

---

## Configuration Reference

### `config.py`

```python
# USB printer IDs (find with lsusb)
DEFAULT_VENDOR_ID  = 0x0483
DEFAULT_PRODUCT_ID = 0x5840

# Modules to run when no CLI flags are provided
DEFAULT_OPTIONS = ["weather", "markets", "quote"]

# Market tickers for --markets (name -> yfinance symbol)
TICKERS = {
    "NIFTY": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK": "^NSEBANK",
    "N50": "NIFTYBEES.NS",
    # Add custom tickers here
}

# RSS feed for news (optional, unused by default)
DEFAULT_RSS_URL = "https://www.thehindu.com/news/national/feeder/default.rss"
```

### Environment Variables (Optional)

```bash
export PAPER_FEED_VENDOR_ID=0x0483
export PAPER_FEED_PRODUCT_ID=0x5840
export PAPER_FEED_CITY="Mumbai"
export PAPER_FEED_RSS_URL="https://feeds.bbci.co.uk/news/rss.xml"
```

> **Note:** Environment variable support is not yet implemented in code — see [Future Ideas](#future-ideas).

---

## Implementation Overview

### Architecture

```
paper-feed/
├── daily_arg.py        # CLI entry point, argument parsing, orchestration
├── config.py           # Central configuration (printer IDs, tickers, defaults)
├── printer.py          # Printer abstraction (USB + TerminalPrinter for --test)
├── function/
│   ├── __init__.py     # Package marker
│   ├── weather.py      # Current + forecast (wttr.in + Open-Meteo)
│   ├── forecast.py     # 7-day forecast formatting
│   ├── markets.py      # Index/ETF performance table
│   ├── stock.py        # Individual ticker deep-dive
│   ├── quote.py        # Random quote (quotable.io)
│   ├── comic.py        # XKCD download + grayscale conversion
│   ├── news.py         # RSS headline fetching
│   ├── text_inp.py     # Custom text printing
│   └── image_inp.py    # Image loading + thermal conversion
└── requirements.txt    # Python dependencies
```

### Data Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  CLI Args   │────▶│ daily_arg.py │────▶│  Printer    │
│  / Config   │     │  (orchestr.) │     │  (USB/Term) │
└─────────────┘     └──────┬───────┘     └──────┬──────┘
                           │                    │
         ┌─────────────────┼────────────────────┘
         ▼                 ▼
   ┌──────────┐      ┌──────────┐
   │ function/│      │ function/│
   │ weather  │      │ markets  │
   │ stock    │      │ quote    │
   │ comic    │  ... │ news     │
   └──────────┘      └──────────┘
         │                 │
         └────────┬────────┘
                  ▼
         ┌──────────────┐
         │  Printer API │  (escpos: text, image, set, ln, cut)
         └──────────────┘
```

### Printer Abstraction (`printer.py`)

- **`create_printer(vid, pid)`** — Returns `escpos.printer.Usb` instance
- **`TerminalPrinter`** — Drop-in replacement for `--test` mode; mimics ESC/POS API (`text`, `set`, `image`, `ln`, `cut`)
- **`print_title(printer, title)`** — Centered, double-width header
- **`hr(printer)`** — Horizontal rule (`---...`)

Each module's `print_*` function receives a printer instance and calls the shared helpers for consistent formatting.

### Adding a New Module

1. Create `function/new_module.py` with a `print_new_module(printer, *args)` function
2. Import and wire it in `daily_arg.py`:
   ```python
   from function.new_module import print_new_module
   # ...
   if args.new_module:
       print_new_module(printer, args.arg1)
   ```
3. Add CLI argument in `parse_args()`
4. (Optional) Add to `DEFAULT_OPTIONS` in `config.py`

---

## Troubleshooting

### Printer Not Found / Permission Denied

```bash
# Linux: Add udev rule for USB access without sudo
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="5840", MODE="0666", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-thermal-printer.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
# Then re-plug printer or reboot
```

### Garbled Output / Wrong Code Page

- Ensure printer supports ESC/POS (most thermal receipt printers do)
- Try setting code page explicitly: `printer.set(codepage='cp437')` (in `printer.py`)
- For non-Latin scripts, you may need a font file and `printer.text()` with custom encoding

### Image Printing Issues

- Images are auto-converted to 1-bit grayscale (mode `L`) in `comic.py` / `image_inp.py`
- Max width: **384 dots** (typical 58mm) or **576 dots** (80mm) — wider images are scaled down
- Use high-contrast images for best results

### Network / API Failures

| Module | API | Failure Mode | Fix |
|--------|-----|--------------|-----|
| Weather | wttr.in / Open-Meteo | Timeout / 5xx | Check internet; APIs have no auth |
| Markets/Stocks | Yahoo Finance (yfinance) | Rate limit / 429 | Add delay; yfinance is unofficial |
| Quotes | quotable.io | Timeout | Retry logic not implemented |
| XKCD | xkcd.com | 404 / network | Comic # may not exist yet |
| News | RSS feed | Parse error | Validate feed URL in config |

### Python Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# If escpos fails on Linux:
sudo apt-get install libusb-1.0-0-dev libudev-dev
pip install --force-reinstall escpos
```

### Windows-Specific Issues

| Issue | Solution |
|-------|----------|
| `USBError: Access denied` | Use Zadig to install libusbK/WinUSB driver |
| `SerialException: Permission denied` | Close other apps using COM port; run as Admin |
| `ModuleNotFoundError: escpos` | `pip install escpos[usb]` |
| Unicode errors in terminal | `chcp 65001` (set UTF-8 code page) |

---

## Testing

### Terminal Test Mode

```bash
# Full feed to terminal
python daily_arg.py --test

# Individual modules
python daily_arg.py --weather --city Tokyo --test
python daily_arg.py --stock AAPL --test
python daily_arg.py --xkcd --test
```

### Syntax Check

```bash
python -m py_compile daily_arg.py config.py printer.py function/*.py
```

### Unit Tests (Future)

See [Issue #22](https://github.com/brick-24/paper-feed/issues/22) — pytest test suite is planned.

---

## Future Ideas

- [ ] **RSS News Headlines** — Configurable feed, category filtering
- [ ] **Calendar Integration** — Google Calendar / CalDAV daily agenda
- [ ] **Todo List Printing** — Todoist, Microsoft To Do, or local file
- [ ] **GitHub Notifications** — Unread notifications summary
- [ ] **Daily Schedule** — Time-blocked agenda from calendar
- [ ] **QR Code Generation** — Wi-Fi, URLs, contact cards
- [ ] **Custom Templates** — YAML/JSON layout definitions
- [ ] **Scheduled Printing** — systemd timer / cron / Windows Task Scheduler
- [ ] **Environment Variable Config** — Override `config.py` via env vars
- [ ] **Plugin System** — Dynamic module discovery
- [ ] **Web UI** — Configure and preview prints from browser
- [ ] **Multi-Printer Support** — Print to multiple printers simultaneously

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes (follow existing code style)
4. Run syntax check: `python -m py_compile $(git diff --name-only --diff-filter=ACMR | grep '\.py$')`
5. Test with `--test` mode
6. Open a Pull Request against `main`

### Code Style

- **Python 3.11+** type hints where practical
- **4-space indentation**, no tabs
- **Line length:** ~100 chars (soft)
- **Imports:** stdlib → third-party → local
- **Docstrings:** Google style for public functions

---

## Related Projects

- [python-escpos](https://github.com/python-escpos/python-escpos) — ESC/POS printer library
- [wttr.in](https://wttr.in) — Weather API (no key required)
- [Open-Meteo](https://open-meteo.com) — Free weather forecast API
- [yfinance](https://github.com/ranaroussi/yfinance) — Yahoo Finance wrapper
- [quotable.io](https://quotable.io) — Quotes API

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Addy Osmani** — Inspiration for structured agent skills
- **ESC/POS community** — Reverse-engineered printer commands
- **Open-Meteo & wttr.in** — Free, no-key weather APIs
- **XKCD** — Randall Munroe for the comics

---

> Built for the joy of holding a personalized newspaper every morning. ☕📰