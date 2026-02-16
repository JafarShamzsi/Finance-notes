# Performance Metrics

Performance metrics are essential for evaluating the results of a backtest and comparing different trading strategies. It's important to look at a variety of metrics to get a complete picture of a strategy's performance.

## Key Performance Metrics

### Sharpe Ratio
- **Formula:** `(Mean of (Portfolio Return - Risk-Free Rate)) / Standard Deviation of (Portfolio Return - Risk-Free Rate))`
- **Interpretation:** Measures the risk-adjusted return of a strategy. A higher Sharpe Ratio indicates a better risk-adjusted return. A common benchmark is a Sharpe Ratio greater than 1.0.

### Sortino Ratio
- **Formula:** `(Mean of (Portfolio Return - Risk-Free Rate)) / Standard Deviation of (Negative Portfolio Returns)`
- **Interpretation:** Similar to the Sharpe Ratio, but it only considers downside volatility. This can be a more useful metric for investors who are more concerned with losses than with overall volatility.

### Calmar Ratio
- **Formula:** `Compounded Annual Growth Rate / Maximum Drawdown`
- **Interpretation:** Measures the return of a strategy relative to its maximum drawdown. A higher Calmar Ratio is better. This metric is particularly useful for evaluating the risk of large losses.

### Maximum Drawdown
- **Definition:** The largest peak-to-trough decline in the value of a portfolio.
- **Interpretation:** A measure of the worst-case loss that a strategy has experienced. This is a critical metric for risk management.

### Compounded Annual Growth Rate (CAGR)
- **Formula:** `(Ending Value / Beginning Value)^(1 / Number of Years) - 1`
- **Interpretation:** The annualized rate of return of an investment, assuming that the profits are reinvested.

### Other Important Metrics
- **Win/Loss Ratio:** The number of winning trades divided by the number of losing trades.
- **Average Win/Average Loss:** The average profit of winning trades divided by the average loss of losing trades.
- **Profit Factor:** Gross Profit / Gross Loss.
- **Time in Market:** The percentage of time that the strategy has an open position in the market.
