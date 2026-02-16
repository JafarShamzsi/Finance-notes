# Lookahead Bias

Lookahead bias is a common and subtle error in backtesting that occurs when the trading algorithm uses information that would not have been available at the time of the trade. This leads to unrealistically optimistic backtest results.

## Common Causes
- **Using future data:** The most obvious form of lookahead bias is using data from the future. For example, using the closing price of a bar to make a decision at the opening of the same bar.
- **Incorrectly adjusted data:** Using historical data that has been adjusted for splits, dividends, or other corporate actions without accounting for the fact that these adjustments were not known at the time.
- **Using information from other assets:** Using information from other assets that would not have been available at the same time. For example, using the closing price of stock B to make a trading decision on stock A, when stock B's closing price is determined after stock A's.

## How to Avoid Lookahead Bias
- **Use point-in-time data:** Ensure that the data used for backtesting is a "point-in-time" snapshot of the market as it existed at that moment.
- **Be careful with indicators:** When using technical indicators, ensure that they are calculated using only data that was available up to that point in time.
- **Code defensively:** Write your backtesting code in a way that explicitly prevents lookahead bias. For example, when iterating through historical data, only use data from previous time steps.
- **Lag your signals:**  A simple and effective method is to lag your trading signals by one bar. If a signal is generated on a given bar, execute the trade on the next bar.
