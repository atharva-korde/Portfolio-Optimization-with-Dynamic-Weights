import numpy as np
import pandas as pd
from optimizer import optimize_portfolio


def run_backtest(
    returns: pd.DataFrame,
    rolling_window: int,
    rebalancing_freq: int,
    risk_free_rate: float,
) -> tuple[pd.Series, pd.Series, pd.DataFrame]:

    portfolio_returns, benchmark_returns = [], []
    rebalancing_dates = []
    weights_history = []

    tickers = returns.columns

    for i in range(rolling_window, len(returns), rebalancing_freq):

        historical_window = returns.iloc[
            i - rolling_window : i
        ]  # The observation period is from i-rolling_window to i-1

        mean_returns = historical_window.mean()
        cov_matrix = historical_window.cov()

        optimal_weights = optimize_portfolio(mean_returns, cov_matrix, risk_free_rate)

        future_returns = returns.iloc[
            i : i + rebalancing_freq
        ].mean()  # Start from i to prevent look-ahead bias

        strategy_returns = optimal_weights.dot(future_returns)
        portfolio_returns.append(strategy_returns)

        equal_weights = np.array(len(tickers) * [1 / len(tickers)])

        benchmark = equal_weights.dot(future_returns)
        benchmark_returns.append(benchmark)

        rebalancing_dates.append(returns.index[i])

        weights_history.append(optimal_weights)

    portfolio_returns = pd.Series(portfolio_returns)
    benchmark_returns = pd.Series(benchmark_returns)
    weights_df = pd.DataFrame(weights_history, columns=tickers, index=rebalancing_dates)

    return (portfolio_returns, benchmark_returns, weights_df)
