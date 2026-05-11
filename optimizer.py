import numpy as np
from scipy.optimize import minimize
from numpy.typing import NDArray

def portfolio_metrics(weights: NDArray[np.float64], mean_returns: NDArray[np.float64], cov_matrix: NDArray[np.float64]) -> tuple[float, float]:
    portfolio_returns = np.sum(weights * mean_returns) * 252
    # Computes the annualized expected returns (252-day period)

    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    # Computes the annualized standard deviation

    return portfolio_returns, portfolio_volatility

def negative_sharpe_ratio(weights: NDArray[np.float64], mean_returns:NDArray[np.float64], cov_matrix:NDArray[np.float64], risk_free_rate:float):
    p_return, p_vol = portfolio_metrics(weights, mean_returns, cov_matrix)

    sharpe_ratio = (p_return - risk_free_rate)/p_vol

    return -sharpe_ratio

# A function to determine those weights maximizing the Sharpe ratio
def optimize_portfolio(mean_returns: NDArray[np.float64], cov_matrix: NDArray[np.float64], risk_free_rate: float) -> NDArray[np.float64]:

    number_of_assets = len(mean_returns)

    constraints = ({"type" : "eq", "fun": lambda x: np.sum(x)-1})
    # The constraint for the weights w_i is (sum w_i = 1)

    initial_weights = number_of_assets * [1/number_of_assets]
    # Use equal weights as an initial guess

    bounds = tuple((0,1) for _ in range(number_of_assets))
    # Note the condition 0 < w_i < 1 for every weight w_i (No short selling)

    max_sharpe_ratio = minimize(negative_sharpe_ratio, initial_weights, args=(mean_returns, cov_matrix, risk_free_rate),
                                method="SLSQP", bounds=bounds, constraints=constraints)
    # SLSQP: Sequential Least Squares
    
    return max_sharpe_ratio.x
