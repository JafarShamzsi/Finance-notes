# Strategies — Map of Content

> Every algorithmic trading strategy exploits a market inefficiency. The key is finding inefficiencies that persist long enough to profit from after [[Fees Commissions and Slippage|transaction costs]].

---

## Strategy Classification

```
                        ┌─── Directional ───┐
                        │                   │
                  ┌─────┤                   ├─────┐
                  │     └───────────────────┘     │
            Trend-Following              Mean Reversion
            [[Momentum Strategies]]      [[Mean Reversion Strategies]]
            [[Trend Following]]          [[Pairs Trading]]
            [[Breakout Strategies]]      [[Statistical Arbitrage]]
                  │                               │
                  └─────┐               ┌─────────┘
                        │               │
                  Market Neutral / Relative Value
                  [[Statistical Arbitrage]]
                  [[Market Making Strategies]]
                        │
                  ┌─────┴─────┐
                  │           │
            Latency-Based   Data-Driven
            [[High-Frequency Trading]]
            [[Machine Learning Strategies]]
            [[Sentiment-Based Strategies]]
```

## By Holding Period

| Strategy | Holding Period | Trades/Day | Capital Needed |
|---|---|---|---|
| [[High-Frequency Trading]] | Microseconds-seconds | 10,000+ | $1M+ |
| [[Market Making Strategies]] | Seconds-minutes | 1,000+ | $500K+ |
| Intraday [[Momentum Strategies]] | Minutes-hours | 10-50 | $25K+ |
| [[Mean Reversion Strategies]] | Hours-days | 1-10 | $10K+ |
| [[Pairs Trading]] | Days-weeks | 1-5 | $50K+ |
| [[Trend Following]] | Weeks-months | 0.1-1 | $100K+ |

## By Edge Source

| Edge | Strategies | Decay Speed |
|---|---|---|
| **Speed** | [[High-Frequency Trading]], latency arb | Fast (arms race) |
| **Statistical** | [[Statistical Arbitrage]], [[Mean Reversion Strategies]] | Medium |
| **Information** | [[Sentiment-Based Strategies]], alt data | Medium-Fast |
| **Behavioral** | [[Momentum Strategies]], overreaction | Slow |
| **Structural** | Index rebalancing, roll yield | Slow |
| **Risk Premia** | [[Trend Following]], carry, value | Very Slow |

## Strategy Development Workflow

1. **Hypothesis** — What inefficiency are you exploiting?
2. **Data** — Collect and clean (see [[Data Engineering MOC]])
3. **Signal** — Define entry/exit rules
4. **Backtest** — Test historically (see [[Backtesting MOC]])
5. **Risk** — Size positions (see [[Risk Management MOC]])
6. **Validate** — Out-of-sample, walk-forward (see [[Walk-Forward Analysis]])
7. **Paper Trade** — Test live without real money
8. **Deploy** — Go live with small size
9. **Monitor** — Track performance, detect decay

## Strategy Categories
- [[05 - Strategies/HFT/High-Frequency Trading|High-Frequency Trading]]
- [[05 - Strategies/Market Making/Market Making Strategies|Market Making]]
- [[05 - Strategies/Mean Reversion/Mean Reversion Strategies|Mean Reversion]]
- [[05 - Strategies/Momentum/Momentum Strategies|Momentum]]
- [[05 - Strategies/Statistical Arbitrage/Statistical Arbitrage|Statistical Arbitrage]]
- [[05 - Strategies/Machine Learning/Machine Learning Strategies|Machine Learning]]
- [[05 - Strategies/Options/Options Strategies for Algos|Options]]

## All Strategy Notes

### Directional
- [[Momentum Strategies]]
- [[Mean Reversion Strategies]]
- [[Trend Following]]
- [[Breakout Strategies]]

### Market Neutral / Relative Value
- [[Statistical Arbitrage]]
- [[Pairs Trading]]
- [[Market Making Strategies]]

### Alpha & Factor
- [[Alpha Research]] — Systematic alpha generation pipeline
- [[Factor Investing]] — Systematic factor harvesting (value, momentum, quality)

### Quantitative
- [[Machine Learning Strategies]]
- [[Sentiment-Based Strategies]]
- [[High-Frequency Trading]]

### Options & Volatility
- [[Options Strategies for Algos]]
- [[Volatility Trading]] — Vol surface, gamma scalping, variance swaps

### Alternative Markets
- [[Crypto Algorithmic Trading]]

---

**Related:** [[Trading Algorithms Master Index]] | [[Backtesting MOC]] | [[Risk Management MOC]] | [[Performance Metrics]] | [[Portfolio Management MOC]]
