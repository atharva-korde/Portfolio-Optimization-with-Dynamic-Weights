# Portfolio Optimization by Dynamic Weights

## Introduction

Let $S_1, S_2, \ldots, S_n$ be $n$ stocks whose returns are denoted by the random variables $R_1, R_2, \ldots, R_n$ respectively. The returns may be percentage returns (used in this project): If the price of stock at times $i-1$ and $i$ is $P_{i-1}$ and $P_i$, then the percentage return at time $i$ is $\frac{P_i - P_{i-1}}{P_i}$, or logarithmic returns, defined at time $i$ by $\log \left(\frac{P_i}{P_{i-1}} \right)$. Let $\mu_i = \mathbb{E}(R_i)$ be the expected returns for $S_i$, where the expectation is calculated over a fixed time period for every stock. (Note that these expectations are obviously not constant over time.) Similarly, let $\sigma_{ij} = \text{Cov}(R_i, R_j)$ be the pairwise covariances in the same time period. For each i, if we have $w_i$ shares of stock $S_i$ giving returns $R$, then the expected return of this portfolio is $\mathbb{E}(R) = \sum_i w_i\mathbb{E}(R_i) = \sum_i w_i \mu_i$ by linearity of expectation. The volatility $\sigma_R$ (mathematically this is just the standard deviation of $R$) can be obtained by a simple calculation of the variance, as the square root of $w^T \Sigma w$, where $w$ is the (column) vector $(w_1, w_2, \ldots, w_n)$ and $\Sigma = (\sigma_{ij})$ is the covariance matrix.

Let $r$ be the risk-free rate. In this project, the objective is to research whether dynamically chaging weights improve the Sharpe ratio of the portfolio. For a fixed period, we find weights $w_1, w_2, \ldots, w_n$ with $w_i \in [0,1]$ for each $i$ and $\sum_i w_i = 1$ so that the Sharpe ratio $\frac{\mathbb{E}(R)- r}{\sigma_R}$ is maximized - roughly speaking, we're trying to minimize volatility while also trying to maximize the net gains in the numerator after accounting for the risk-free rate. In other common models like the Markovitz model, the objective is to maximize a utility function of the form $\mathbb{E}(R) - a \sigma_R$ for some $a > 0$ depending on how risk-averse you want the portfolio to be. To annualize the Sharpe ratio, we multiply by $\sqrt{\frac{252}{n}}$ where $ n $ is the period of days used to compute the Sharpe ratio.

Because of the note in the first paragraph, that the expected returns and volatilities change over time, the optimal weights are also going to be time-dependent. The strategy followed here is rather natural: Observe historical data for a long period (252 days, for example), find optimal weights for maximizing the Sharpe ratio during this period, and then build the portfolio using these optimal weights for a short period in future (7 days, for example). The end of the short period is when we change weights to fit in line with the 'new historical data' - We will use an optimal weight vector $w$ for days 253-259 based on historical data from days 1-252, then we change to a new optimal weight vector $w'$ for days 260-266 based on historical data now from days 8-259, and so on. This way, we prevent look-ahead bias. (This is the content of the backtest.py script.) We can compare this with the naive strategy of keeping equal weights $w_i = \frac{1}{n}$ for all $i$ throughout history. 

In our example, we consider five stocks of big tech: Apple, Amazon, Google, Meta, and Microsoft. We compare the naive strategy with the rebalancing strategy, assuming constant risk-free rate throughout.

## Results

For dynamically changing weights, the following table shows the values of the annualized Sharpe Ratios for various rebalancing frequencies as columns with various historical observation periods as rows:

|     |        1 |        7 |       14 |       21 |       42 |
|----:|---------:|---------:|---------:|---------:|---------:|
| 126 | 0.984228 | 1.22924  | 1.22195  | 1.13911  | 1.03428  |
| 252 | 1.04232  | 1.25947  | 1.33871  | 1.24521  | 1.2085   |
| 504 | 0.826075 | 0.926745 | 0.865436 | 0.897176 | 0.891744 |

For constant uniform weights $w_i = \frac{1}{5}$ for all $i$, here is the same table:

|     |       1 |       7 |      14 |      21 |      42 |
|----:|--------:|--------:|--------:|--------:|--------:|
| 126 | 1.05563 | 1.13716 | 1.19431 | 1.13497 | 1.2554  |
| 252 | 1.03786 | 1.11945 | 1.17162 | 1.11724 | 1.23254 |
| 504 | 0.93287 | 1.0074  | 1.05287 | 1.00445 | 1.10261 |

We observe that changing weights too frequently is a worse option than constant weights. This is rather intuitive as excessive rebalancing is too 'noisy'. We also observe that a longer lookback period is worse when dynamically changing weights - which is an indication that the optimal weights for very-long-term data may not be optimal short-term future trends due to overfitting. For the best Sharpe ratios, a lookback period of 252 days (one trading year) seems optimal, with those trends applicable in the next 7-21 days.

Note that the Sharpe ratio values all lie within practical bounds without being obscenely high. We have made many simplifying assumptions in this project, including the assumption that there are no transaction costs. Therefore, these numbers will be lower in practice, however, we do obtain general experimental evidence from these numbers.
