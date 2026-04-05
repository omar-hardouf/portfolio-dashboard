import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# --- CONFIG ---
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
START_DATE = "2022-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")
DB_PATH = "portfolio.db"

# --- FETCH ---
def fetch_prices(tickers, start, end):
    print(f"Fetching data for: {tickers}")
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True)
    prices = raw["Close"]
    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "date"
    print(f"✓ Fetched {len(prices)} rows from {prices.index[0].date()} to {prices.index[-1].date()}")
    return prices

# --- STORE ---
def save_to_db(prices, db_path):
    engine = create_engine(f"sqlite:///{db_path}")
    prices.to_sql("prices", con=engine, if_exists="replace", index=True)
    print(f"✓ Saved to {db_path} → table: 'prices'")

# --- LOAD ---
def load_from_db(db_path):
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql("SELECT * FROM prices", con=engine, index_col="date", parse_dates=["date"])
    print(f"✓ Loaded {len(df)} rows from database")
    return df

# --- RUN ---
if __name__ == "__main__":
    prices = fetch_prices(TICKERS, START_DATE, END_DATE)
    save_to_db(prices, DB_PATH)

    # Verify by reloading
    loaded = load_from_db(DB_PATH)
    print("\nPreview:")
    print(loaded.tail())