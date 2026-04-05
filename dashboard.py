import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_fetcher import load_from_db
from metrics import calc_returns, calc_cumulative_returns, full_summary

def build_dashboard(prices):
    returns = calc_returns(prices)
    cum_returns = calc_cumulative_returns(returns)
    summary = full_summary(prices)
    corr = returns.corr()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Cumulative Returns",
            "Annualised Metrics",
            "Rolling 30d Volatility",
            "Correlation Matrix"
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    # --- 1. Cumulative Returns ---
    for ticker in cum_returns.columns:
        fig.add_trace(
            go.Scatter(x=cum_returns.index, y=cum_returns[ticker],
                       name=ticker, mode="lines"),
            row=1, col=1
        )

    # --- 2. Annualised Metrics Bar Chart ---
    metrics_to_plot = ["Annualised Return", "Annualised Vol", "Sharpe Ratio"]
    for metric in metrics_to_plot:
        fig.add_trace(
            go.Bar(name=metric, x=summary.index, y=summary[metric],
                   text=summary[metric].round(3), textposition="outside"),
            row=1, col=2
        )

    # --- 3. Rolling 30d Volatility ---
    rolling_vol = returns.rolling(30).std() * np.sqrt(252)
    for ticker in rolling_vol.columns:
        fig.add_trace(
            go.Scatter(x=rolling_vol.index, y=rolling_vol[ticker],
                       name=ticker, mode="lines", showlegend=False),
            row=2, col=1
        )

    # --- 4. Correlation Heatmap ---
    fig.add_trace(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdBu",
            zmin=-1, zmax=1,
            text=corr.round(2).values,
            texttemplate="%{text}",
            showscale=True
        ),
        row=2, col=2
    )

    fig.update_layout(
        title="Portfolio Analytics Dashboard",
        height=800,
        template="plotly_dark",
        legend=dict(orientation="h", y=-0.15)
    )

    fig.show()
    fig.write_html("dashboard.html")
    print("✓ Dashboard saved to dashboard.html")

if __name__ == "__main__":
    prices = load_from_db("portfolio.db")
    build_dashboard(prices)