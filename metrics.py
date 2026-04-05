import pandas as pd
import numpy as np
from data_fetcher import load_from_db

RISK_FREE_RATE = 0.04  # Annual, ~current US T-bill rate

def calc_returns(prices):
    return prices.pct_change().dropna()

def calc_cumulative_returns(returns):
    return (1 + returns).cumprod() - 1

def calc_annualised_volatility(returns):
    return returns.std() * np.sqrt(252)

def calc_sharpe_ratio(returns, rfr=RISK_FREE_RATE):
    excess = returns.mean() * 252 - rfr
    vol = calc_annualised_volatility(returns)
    return excess / vol

def calc_max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    return drawdown.min()

def calc_annualised_return(returns):
    n_years = len(returns) / 252
    total_return = (1 + returns).prod()
    return total_return ** (1 / n_years) - 1

def full_summary(prices):
    returns = calc_returns(prices)
    
    summary = pd.DataFrame({
        "Annualised Return":   calc_annualised_return(returns),
        "Annualised Vol":      calc_annualised_volatility(returns),
        "Sharpe Ratio":        calc_sharpe_ratio(returns),
        "Max Drawdown":        calc_max_drawdown(returns),
    })
    return summary.round(4)

if __name__ == "__main__":
    prices = load_from_db("portfolio.db")
    summary = full_summary(prices)
    print("\n--- Portfolio Metrics ---")
    print(summary.to_string())