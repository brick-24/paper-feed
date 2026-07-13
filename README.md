``` ████   ███  ████  █████ ████       █████ █████ █████ ████
█   █ █   █ █   █ █     █   █      █     █     █     █   █
████  █████ ████  ████  ████  ████ ████  ████  ████  █   █
█     █   █ █     █     █  █       █     █     █     █   █
█     █   █ █     █████ █   █      █     █████ █████ ████
```

A personal thermal newspaper that automatically generates a daily briefing.

Paper-feed has useful modules such as weather, market metrics, quotes, XKCD comics, stock summaries, news headlines, and more — printing directly to a USB ESC/POS thermal printer. It can also print arbitrary text and images, making it a lightweight dashboard on paper.

## Features

- **Weather forecast** for any city (powered by wttr.in)
- **Weekly weather forecast** (7-day, powered by Open-Meteo)
- **Market performance** summary (NSE/BSE indices & ETFs)
- **Individual stock lookup** with returns, market cap, P/E, dividend yield, 52-week range
- **Random inspirational quotes** (via Quotable API)
- **Latest XKCD comic** (image + title)
- **RSS news headlines** (The Hindu business/finance feed)
- **Print custom text** and **local images**
- **Terminal test mode** (no printer required)

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.13+ (CI tests on 3.11, 3.12, 3.13) |
| **Printer** | USB ESC/POS thermal printer (or `--test` mode for terminal output) |
| **OS** | Linux, macOS, Windows (see [Printer Setup](#printer-setup--troubleshooting)) |
| **Dependencies** | See `requirements.txt` (requests, yfinance, feedparser, Pillow, escpos, etc.) |

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Printer Setup & Troubleshooting

### Find your printer's USB IDs

**Linux/macOS:**
```bash
lsusb
# Look for your printer, e.g.:
# Bus 001 Device 004: ID 0483:5840 STMicroelectronics Virtual COM Port
# Vendor ID = 0x0483, Product ID = 0x5840
```

**Windows:**
1. Open Device Manager → Universal Serial Bus controllers
2. Right-click your printer → Properties → Details → Hardware Ids
3. Look for `VID_XXXX&PID_YYYY` (hex values)

### Configure the printer IDs

Edit `config.py` and set:
```python
DEFAULT_VENDOR_ID  = 0x0483  # Your vendor ID
DEFAULT_PRODUCT_ID = 0x5840  # Your product ID
```

### Linux USB permissions

If you get "Permission denied" or "Access denied":
```bash
# Add udev rule (replace IDs with yours)
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="5840", MODE="0666"' \
  | sudo tee /etc/udev/rules.d/99-thermal-printer.rules

sudo udevadm control --reload-rules && sudo udevadm trigger
# Then unplug/replug the printer
```

### Windows serial/COM port setup

On Windows, ESC/POS printers often appear as COM ports rather than USB bulk endpoints. If the USB approach doesn't work:

1. Find the COM port in Device Manager (e.g., `COM3`)
2. The `escpos` library supports serial connections. You may need to modify `printer.py`:
   ```python
   from escpos.printer import Serial
   printer = Serial(devfile='COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1)
   ```
3. Alternatively, use a USB-to-serial driver that exposes bulk endpoints.

> **Note:** Windows USB printing with `python-escpos` can be finicky. The `--test` mode (terminal output) works on all platforms and is recommended for development.

### Common issues

| Symptom | Fix |
|---------|-----|
| `USBError: Access denied` | Add udev rule (Linux) or run as admin (Windows) |
| `USBError: Entity not found` | Wrong vendor/product ID — verify with `lsusb` |
| Printer prints garbage | Check baud rate / encoding; try `--test` mode first |
| `ModuleNotFoundError: escpos` | Run `pip install -r requirements.txt` |

---

## Installation

```bash
git clone https://github.com/brick-24/paper-feed.git
cd paper-feed
pip install -r requirements.txt

# Edit config.py with your printer's USB IDs
vim config.py
```

---

## Usage

Run with no arguments to print the **default feed** (weather + markets + quote):

```bash
python daily_arg.py
```

### Print specific sections

| Flag | Description | Example |
|------|-------------|---------|
| `--weather` | Current weather | `python daily_arg.py --weather` |
| `--weather --city "London"` | Weather for a city | `python daily_arg.py --weather --city London` |
| `--forecast` | 7-day forecast | `python daily_arg.py --forecast --city Tokyo` |
| `--markets` | Market summary | `python daily_arg.py --markets` |
| `--stock AAPL` | Single stock details | `python daily_arg.py --stock AAPL` |
| `--stock RELIANCE.NS` | Indian stock (NSE) | `python daily_arg.py --stock RELIANCE.NS` |
| `--quote` | Random quote | `python daily_arg.py --quote` |
| `--xkcd` | Latest XKCD comic | `python daily_arg.py --xkcd` |
| `--news` | RSS headlines | `python daily_arg.py --news` |
| `--text "Hello"` | Custom text | `python daily_arg.py --text "Hello, World!"` |
| `--image path.png` | Local image | `python daily_arg.py --image assets/logo.png` |
| `--test` | Terminal output (no printer) | `python daily_arg.py --test --weather` |

### Combine multiple flags

```bash
# Full morning briefing
python daily_arg.py --weather --forecast --markets --stock AAPL --quote --news --xkcd

# Quick stock check
python daily_arg.py --stock TSLA --stock MSFT --test
```

> **Note:** Multiple `--stock` flags are not yet supported in a single run. Run separately or add to default feed via `config.py`.

---

## Configuration

All user-facing settings live in `config.py`:

```python
# Printer USB IDs (required for hardware printing)
DEFAULT_VENDOR_ID  = 0x0483
DEFAULT_PRODUCT_ID = 0x5840

# Default feed sections (run with no args)
DEFAULT_OPTIONS = ["weather", "markets", "quote"]

# Market tickers for --markets (name -> yfinance symbol)
TICKERS = {
    "NIFTY": "^NSEI",
    "SENSX": "^BSESN",
    "BANK":  "^NSEBANK",
    "N50":   "NIFTYBEES.NS",
    # ...add your own
}

# RSS feed for --news (default: The Hindu business)
# Change in function/news.py: RSS_URL = "your-feed-url"
```

### Customizing the default feed

Edit `DEFAULT_OPTIONS` in `config.py`. Valid options:
`weather`, `markets`, `quote`, `forecast`, `xkcd`, `news`

Example — add forecast and news to daily print:
```python
DEFAULT_OPTIONS = ["weather", "forecast", "markets", "quote", "news"]
```

### Adding custom stock tickers

Add entries to `TICKERS` dict in `config.py`:
```python
TICKERS = {
    # ...existing...
    "MYSTOCK": "MYTICKER.NS",  # NSE suffix for Indian stocks
    "SPY":     "SPY",          # US ETF
}
```

Then `python daily_arg.py --markets` will include them.

---

## Project Structure

```
paper-feed/
├── daily_arg.py          # CLI entry point, argument parsing, orchestration
├── config.py             # User configuration (printer IDs, tickers, defaults)
├── printer.py            # Printer abstraction (USB + TerminalPrinter for --test)
├── requirements.txt      # Python dependencies
├── function/
│   ├── __init__.py
│   ├── weather.py        # Current weather (wttr.in)
│   ├── forecast.py       # 7-day forecast (Open-Meteo)
│   ├── markets.py        # Market summary (yfinance)
│   ├── stock.py          # Single stock details (yfinance)
│   ├── quote.py          # Random quote (quotable.io)
│   ├── comic.py          # XKCD comic (xkcd.com + Pillow)
│   ├── news.py           # RSS headlines (feedparser)
│   ├── text_inp.py       # Custom text printing
│   └── image_inp.py      # Local image printing (Pillow)
└── tests/                # Pytest suite (43 tests, mocks external APIs)
    ├── conftest.py
    ├── test_config.py
    ├── test_printer.py
    ├── test_weather.py
    ├── test_forecast.py
    ├── test_markets.py
    ├── test_stock.py
    ├── test_quote.py
    ├── test_news.py
    ├── test_daily_arg.py
    └── test_comic.py
```

### Module responsibilities

| Module | Purpose | External APIs |
|--------|---------|---------------|
| `daily_arg.py` | CLI parsing, printer init, feature orchestration | — |
| `config.py` | Central configuration (IDs, tickers, defaults) | — |
| `printer.py` | `create_printer()` (USB), `TerminalPrinter` (test mode), formatting helpers | `python-escpos` |
| `weather.py` | Current conditions + near-term forecast | `wttr.in` (JSON) |
| `forecast.py` | 7-day forecast with codes | `open-meteo.com`, `geocoding-api.open-meteo.com` |
| `markets.py` | Index/ETF performance table | `yfinance` |
| `stock.py` | Single stock: returns, financials, 52wk range | `yfinance` |
| `quote.py` | Random inspirational quote | `api.quotable.io` |
| `comic.py` | Latest XKCD (download, grayscale, print) | `xkcd.com`, `Pillow` |
| `news.py` | RSS feed parsing & formatting | `feedparser` |
| `text_inp.py` / `image_inp.py` | User-provided content | — |

---

## Testing

Run the test suite (mocks all external APIs):

```bash
pip install -r requirements-test.txt  # pytest, pytest-mock, requests-mock, freezegun
pytest tests/ -v
```

Expected output: **43 tests passing** across all modules.

### CI

GitHub Actions workflow (`.github/workflows/test.yml`) runs tests on Python 3.11, 3.12, 3.13 with coverage reporting.

---

## Future Ideas

Community contributions welcome! Open an issue with prefix `feature: ...`

- Calendar integration (iCal/Google Calendar → daily agenda print)
- Todo list printing (from local file or Todoist/Notion API)
- GitHub notifications summary
- Daily schedule / time-blocking printout
- QR codes (WiFi credentials, URLs, contact cards)
- Custom templates / layout engine
- Automatic scheduled printing (systemd timer / cron / Windows Task Scheduler)
- Config file (YAML/TOML) instead of editing `config.py`
- Multiple printer profiles
- Battery/power status for portable printers

See [issue #7](https://github.com/brick-24/paper-feed/issues/7) for the original documentation request that inspired this README expansion.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make changes with tests
4. Run `pytest tests/ -v` and `python -m py_compile $(git diff --name-only --diff-filter=ACMR | grep '\.py$')`
5. Open a PR against `brick-24/paper-feed:main`

Please keep PRs focused and reference related issues.

---

## License

MIT — use freely in your projects.