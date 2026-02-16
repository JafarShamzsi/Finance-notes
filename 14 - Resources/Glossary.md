# Glossary

Quick reference for quant finance terminology.

---

## A

- **Alpha** — Excess return above a benchmark, risk-adjusted. The goal of every quant strategy. See [[Performance Attribution]].
- **ATS (Alternative Trading System)** — Dark pool or electronic venue that isn't a registered exchange.
- **AUM (Assets Under Management)** — Total market value of assets managed by a fund.

## B

- **Basis Point (bp)** — 0.01%. 100 bps = 1%.
- **Beta** — Sensitivity of an asset's returns to the market. Beta of 1.2 = moves 1.2% per 1% market move. See [[Factor Models]].
- **Bid-Ask Spread** — Difference between best buy and sell price. See [[Bid-Ask Spread]].
- **Black-Scholes** — Option pricing model assuming geometric Brownian motion. See [[Stochastic Calculus]].

## C

- **Cointegration** — Two non-stationary series that share a stationary linear combination. Basis of [[Pairs Trading]]. See [[Statistical Arbitrage]].
- **Convexity** — Second derivative of price with respect to yield (bonds) or non-linear payoff structure.
- **CVaR (Conditional VaR)** — Expected loss beyond VaR. Also called Expected Shortfall. See [[Value at Risk (VaR)]].

## D

- **Delta** — Rate of change of option price with respect to underlying price.
- **Drawdown** — Peak-to-trough decline. Maximum drawdown = worst such decline. See [[Drawdown Management]].
- **Duration** — Sensitivity of bond price to interest rate changes.

## F

- **Factor** — Systematic risk/return driver (market, size, value, momentum). See [[Factor Models]].
- **Fat Tails** — Return distributions with more extreme events than normal distribution predicts. See [[Tail Risk and Black Swans]].
- **FIX Protocol** — Financial Information eXchange — standard messaging for order routing. See [[Connectivity]].

## G

- **Gamma** — Rate of change of delta. Second derivative of option price w.r.t. underlying.
- **GBM (Geometric Brownian Motion)** — Standard model for stock prices. See [[Stochastic Calculus]].
- **Greeks** — Option sensitivities: Delta, Gamma, Theta, Vega, Rho.

## H

- **Hedge Ratio** — Number of units of hedging instrument per unit of exposure. In pairs trading, the cointegration coefficient.
- **HFT (High-Frequency Trading)** — Trading at microsecond/millisecond timescales. See [[High-Frequency Trading]].

## I

- **Information Ratio** — Active return / tracking error. Measures skill of active management. See [[Performance Attribution]].
- **IV (Implied Volatility)** — Volatility implied by option market prices via Black-Scholes.

## K

- **Kelly Criterion** — Optimal fraction of capital to bet. See [[Kelly Criterion]].

## L

- **Lambda** — Kyle's lambda = price impact coefficient. Measures how much price moves per unit of order flow.
- **Latency** — Time delay. In trading: order-to-fill time. See [[High-Frequency Trading Infrastructure]].
- **Liquidity** — Ability to trade without significant price impact. See [[Liquidity]].

## M

- **Market Cap** — Share price × shares outstanding. Total value of a public company.
- **Market Impact** — Price change caused by your own trading. See [[Market Impact]].
- **Market Making** — Quoting buy and sell prices to profit from the spread. See [[Market Making Strategies]].
- **Mean Reversion** — Tendency of prices to return to a long-term average. See [[Mean Reversion Strategies]].
- **Momentum** — Tendency of recent winners to continue winning. See [[Momentum Strategies]].

## N

- **NBBO** — National Best Bid and Offer. Best prices across all US exchanges. See [[Reg NMS]].

## O

- **Order Book** — List of all outstanding buy and sell orders. See [[Order Book Dynamics]].
- **Overfitting** — Model learns noise instead of signal. #1 enemy of quants. See [[Overfitting]].

## P

- **P&L** — Profit and Loss.
- **PCA** — Principal Component Analysis. Statistical factor extraction. See [[Factor Models]].
- **Position Sizing** — How much capital to allocate per trade. See [[Position Sizing]].

## R

- **Risk Parity** — Portfolio allocation where each asset contributes equal risk. See [[Portfolio Optimization]].
- **RV (Realized Volatility)** — Actual historical volatility computed from returns.

## S

- **Sharpe Ratio** — (Return - Risk-free) / Volatility. Reward per unit of risk. See [[Performance Attribution]].
- **Slippage** — Difference between expected and actual execution price. See [[Fees Commissions and Slippage]].
- **Stat Arb** — Statistical Arbitrage. See [[Statistical Arbitrage]].
- **Stationarity** — Statistical properties (mean, variance) don't change over time. Required for many models.

## T

- **TCA** — Transaction Cost Analysis. Measuring execution quality. See [[Transaction Cost Analysis]].
- **Tick** — Minimum price increment. $0.01 for US stocks above $1.
- **TWAP** — Time-Weighted Average Price. Execution algorithm. See [[TWAP Algorithm]].

## V

- **VaR** — Value at Risk. Maximum loss at given confidence level. See [[Value at Risk (VaR)]].
- **Vega** — Sensitivity of option price to implied volatility.
- **Volatility** — Standard deviation of returns. Can be realized (historical) or implied (from options).
- **VWAP** — Volume-Weighted Average Price. Benchmark and execution algorithm. See [[VWAP Algorithm]].

## Z

- **Z-score** — Number of standard deviations from the mean. Used in [[Mean Reversion Strategies]] and [[Statistical Arbitrage]] for signal generation.

---

## Related Notes
- [[Resources MOC]] — Parent note
- [[Trading Algorithms Master Index]] — Full vault index
