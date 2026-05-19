import pandas as pd
from dataloader import load_price_data, compute_returns
from backtest import run_backtest
from visualizations import plot_cumulative_returns, plot_weights
from var_config import *


def annualized_metrics(
    returns: pd.DataFrame, period_length: int
) -> tuple[float, float, float]:

    annual_return = returns.mean() * (252 / period_length)
    annual_volatility = returns.std() * ((252 / period_length) ** 0.5)
    sharpe_ratio = annual_return / annual_volatility
    return (annual_return, annual_volatility, sharpe_ratio)


def main(printit=False):

    print("Downloading data...")

    prices = load_price_data(TICKERS, START_DATE, END_DATE)
    returns = compute_returns(prices)

    print("Running backtests...")

    strategy_list = []  # List of dictionaries to store Sharpe Ratios from rebalancing
    benchmark_list = []  # List of dictionaries to store Sharpe Ratios from equal weights

    for ROLLING_WINDOW in ROLLING_WINDOW_OPTIONS:

        strategy_dict = {}
        benchmark_dict = {}

        for REBALANCING_FREQ in REBALANCING_FREQ_OPTIONS:

            strategy_returns, benchmark_returns, weights_df = run_backtest(
                returns, ROLLING_WINDOW, REBALANCING_FREQ, RISK_FREE_RATE
            )

            strategy_metrics = annualized_metrics(strategy_returns, REBALANCING_FREQ)
            benchmark_metrics = annualized_metrics(benchmark_returns, REBALANCING_FREQ)

            strategy_dict[REBALANCING_FREQ] = strategy_metrics[2]
            benchmark_dict[REBALANCING_FREQ] = benchmark_metrics[2]

        strategy_list.append(strategy_dict)
        benchmark_list.append(benchmark_dict)

    strategy_df = pd.DataFrame(strategy_list)
    strategy_df.index = ROLLING_WINDOW_OPTIONS

    benchmark_df = pd.DataFrame(benchmark_list)
    benchmark_df.index = ROLLING_WINDOW_OPTIONS

    print("Process complete!")

    if printit:
        print(strategy_df)
        print(benchmark_df)

    return strategy_df, benchmark_df


if __name__ == "__main__":
    main()
