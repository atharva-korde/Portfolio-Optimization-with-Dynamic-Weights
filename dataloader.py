import yfinance as yf
import pandas as pd

# Download closing prices for tickers
def load_price_data(tickers: list[str], start:str, end:str) -> pd.DataFrame:
    prices = yf.download(tickers, start=start, end=end)["Close"]

    return prices.dropna()

def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:

    return prices.pct_change().dropna()