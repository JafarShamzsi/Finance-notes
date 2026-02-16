# Survivorship Bias

Survivorship bias is a common type of selection bias in finance that occurs when a dataset only includes "surviving" or "successful" entities, while excluding "failed" or "delisted" entities. This leads to an overestimation of historical performance and can make trading strategies appear more profitable than they actually are.

## Examples in Finance
- **Stock market indices:** If a backtest is performed on the current constituents of the S&P 500, it will be subject to survivorship bias because it excludes companies that were once in the index but have since been removed due to bankruptcy, merger, or underperformance.
- **Hedge fund databases:** Hedge fund databases often only include funds that are still active, excluding those that have closed down. This can lead to an overly optimistic view of hedge fund performance.

## The Impact of Survivorship Bias
- **Inflated returns:** By excluding failed companies, the average returns of the dataset are artificially inflated.
- **Underestimated risk:** The dataset does not capture the risk of failure, leading to an underestimation of the overall risk of the investment strategy.

## How to Avoid Survivorship Bias
- **Use point-in-time data:** Use historical data that includes all companies that were in the investment universe at each point in time, including those that have since been delisted.
- **Be wary of back-filled data:** When a new stock is added to an index, its historical data is often "back-filled". Be careful not to use this data in a way that would introduce survivorship bias.
- **Use high-quality data sources:** Use data from reputable vendors that provide "point-in-time" data and are careful to avoid survivorship bias.
