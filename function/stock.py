import yfinance as yf
from printer import hr, print_title

def calculate_returns(ticker):
    hist = yf.Ticker(ticker).history(period="1y")
    closes = hist["Close"].dropna()
    
    if len(closes) < 22:
        raise ValueError("Not enough history")
    
    current = closes.iloc[-1]
    
    returns = {
        "week": ((current - closes.iloc[-6]) / closes.iloc[-6])*100,
        "month":((current - closes.iloc[-22])/closes.iloc[-22])*100,
    }
    
    
    if len(closes) >= 252:
        returns["year"] = ((current - closes.iloc[-252]) / closes.iloc[-252]) * 100
    else:
        returns["year"] = ((current - closes.iloc[0]) / closes.iloc[0]) * 100

    return returns

def get_financials(ticker):
    info = yf.Ticker(ticker).info
    
    return {
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "dividend_yield": info.get("dividendYield"),
        "high_52wk": info.get("fiftyTwoWeekHigh"),
        "low_52wk": info.get("fiftyTwoWeekLow"),
    }
    
def format_market_cap(value):
    if value is None:
        return "N/A"
    for unit in ["","K","M","B","T"]:
        if abs(value)<1000:
            return f"{value:.1f}{unit}"
        value/=1000
    return f"{value:.1f}Q"

def print_stock(printer, ticker):
    print_title(printer, f"{ticker.upper()}:")
    hr(printer)
     
    try:
        returns = calculate_returns(ticker)
        fin = get_financials(ticker)
    except Exception:
        printer.text("Could not fetch data for this ticker\n")
        printer.ln()
        return
    printer.text(
        f"Week: {returns['week']:+.1f}%  "
        f"Month: {returns['month']:+.1f}%  "
        f"Year: {returns['year']:+.1f}%\n"
    )
    printer.text(f"Market Cap: {format_market_cap(fin['market_cap'])}\n")
    printer.text(f"P/E Ratio:  {fin['pe_ratio'] if fin['pe_ratio'] else 'N/A'}\n")
    
    if fin["dividend_yield"]:
        printer.text(f"Div yield: {fin['dividend_yield']:.2f}%\n")
        
    printer.text(f"52wk High: {fin['high_52wk']}\n")
    printer.text(f"52wk Low: {fin['low_52wk']}\n")
    
    printer.ln()