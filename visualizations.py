import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# A function to compare cumulative returns of the naive and rebalancing strategies
def plot_cumulative_returns(portfolio_returns: pd.Series, benchmark_returns: pd.Series):

    portfolio_growth = (1 + portfolio_returns).cumprod()
    benchmark_growth = (1 + benchmark_returns).cumprod()

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_growth, label="Optimized Portfolio")
    plt.plot(benchmark_growth, label="Equal Weight Benchmark")
    plt.title("Portfolio Performance")
    plt.xlabel("Time")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.grid(True)
    plt.show()


# A function to plot the distribution of weights over time
def plot_weights(weights_df):

    weights_df.plot(kind="area", stacked=True, figsize=(12, 6))
    plt.title("Dynamic Portfolio Weights")
    plt.ylabel("Weight")
    plt.xlabel("Date")
    plt.grid(True)
    plt.show()


# A function to plot Sharpe Ratios for various rebalancing frequencies with a fixed rolling window, as a grouped bar graph
def sharpe_ratio_bar_graph(
    strategy_series: pd.Series, benchmark_series: pd.Series, rolling_window: int
):

    plt.figure(figsize=(18, 10))
    w, x = 0.4, np.arange(len(strategy_series))
    plt.bar(x - w / 2, strategy_series, w, label="Optimized Portfolio")
    plt.bar(x + w / 2, benchmark_series, w, label="Benchmark")
    plt.xticks(x, strategy_series.index)
    plt.xlabel("Rebalancing Frequencies")
    plt.ylabel("Sharpe Ratio")
    plt.title(f"Lookback Period = {rolling_window}")
    plt.legend()
    plt.show()
