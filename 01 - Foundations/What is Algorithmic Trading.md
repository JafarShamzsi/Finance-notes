# What is Algorithmic Trading

**Algorithmic trading** (algo trading) is the use of computer programs and mathematical models to execute trades automatically based on predefined rules, signals, and conditions.

---

## Core Concept

An algorithm takes **inputs** (price, volume, time, indicators, news) and produces **outputs** (buy/sell/hold decisions with specific quantities, prices, and timing).

```
Market Data → Signal Generation → Risk Check → Order Generation → Execution
```

## Why Algorithmic Trading?

| Advantage | Explanation |
|---|---|
| **Speed** | Executes in microseconds vs. human seconds |
| **Discipline** | No emotional bias — follows rules exactly |
| **Backtestability** | Can test on historical data before risking capital |
| **Scalability** | Monitor thousands of instruments simultaneously |
| **Consistency** | Same conditions → same actions every time |
| **Cost** | Reduced transaction costs via smart execution |

## Types of Algorithmic Trading

1. **Execution Algorithms** — Minimize market impact (see [[TWAP Algorithm]], [[VWAP Algorithm]])
2. **Signal-Based / Alpha Generation** — Generate profit signals (see [[Momentum Strategies]], [[Mean Reversion Strategies]])
3. **Market Making** — Provide liquidity for bid-ask spread capture (see [[Market Making Strategies]])
4. **Statistical Arbitrage** — Exploit statistical mispricings (see [[Statistical Arbitrage]])
5. **High-Frequency Trading** — Ultra-low latency, high volume (see [[High-Frequency Trading]])

## The Algorithmic Trading Pipeline

```
1. Research & Hypothesis
2. Data Collection        → [[Market Data Sources]]
3. Feature Engineering    → [[Feature Engineering for Trading]]
4. Strategy Development   → [[Strategies MOC]]
5. Backtesting           → [[Backtesting MOC]]
6. Risk Management       → [[Risk Management MOC]]
7. Paper Trading
8. Live Deployment       → [[Trading System Architecture]]
9. Monitoring & Tuning   → [[Monitoring and Alerting]]
```

## Key Metrics for Algo Performance

- **Sharpe Ratio** — Risk-adjusted return (see [[Performance Metrics]])
- **Maximum Drawdown** — Worst peak-to-trough decline (see [[Drawdown Management]])
- **Win Rate** — Percentage of profitable trades
- **Profit Factor** — Gross profit / Gross loss
- **Alpha** — Excess return above benchmark (see [[Alpha and Beta]])

## Who Uses Algorithmic Trading?

- **Hedge Funds** — Renaissance Technologies, Two Sigma, DE Shaw, Citadel
- **Investment Banks** — J.P. Morgan, Goldman Sachs, Morgan Stanley
- **Proprietary Trading Firms** — Jane Street, Jump Trading, Virtu Financial
- **Retail Traders** — Using platforms like [[QuantConnect Platform]], Interactive Brokers

## Common Pitfalls

- [[Overfitting and Curve Fitting]] — Strategy works on historical data but fails live
- [[Look-Ahead Bias]] — Accidentally using future information in backtests
- [[Survivorship Bias]] — Only testing on stocks that still exist
- Ignoring [[Fees Commissions and Slippage]]
- Ignoring [[Market Impact]]

---

**Related:** [[Financial Markets Overview]] | [[Strategies MOC]] | [[Backtesting MOC]] | [[Trading System Architecture]]
