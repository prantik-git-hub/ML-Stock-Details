# app/utils.py

import yfinance as yf

def fetch_stock_data(ticker):
    """
    Fetch historical stock data for the given ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        return hist
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def fetch_fundamentals(ticker):
    """
    Fetch basic fundamentals like P/E, EPS, etc. for the given ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "company_name": info.get("longName"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
        }
    except Exception as e:
        print(f"Error fetching fundamentals: {e}")
        return {}
