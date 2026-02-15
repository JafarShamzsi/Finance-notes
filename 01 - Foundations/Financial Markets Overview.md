# Financial Markets Overview

Financial markets are venues where buyers and sellers trade financial instruments. Understanding their structure is essential before building any trading algorithm.

---

## Market Types

### By Instrument
| Market | Instruments | Key Exchanges |
|---|---|---|
| **Equities** | Stocks, ETFs | NYSE, NASDAQ, LSE, TSE |
| **Fixed Income** | Bonds, Treasuries | OTC, CME |
| **Forex (FX)** | Currency pairs | Decentralized (interbank) |
| **Commodities** | Oil, Gold, Wheat | CME, ICE, LME |
| **Derivatives** | Options, Futures, Swaps | CBOE, CME, Eurex |
| **Crypto** | BTC, ETH, tokens | Binance, Coinbase, Kraken |

### By Structure
- **Exchange-Traded** — Centralized, regulated, transparent order book
- **Over-the-Counter (OTC)** — Bilateral, less transparent, customizable
- **Dark Pools** — Private exchanges, hidden [[Liquidity]], reduced [[Market Impact]]
- **Electronic Communication Networks (ECN)** — Electronic matching

## How a Trade Happens

```
Trader → Broker → Exchange/Venue → Matching Engine → Counterparty
                                  ↓
                           Clearinghouse
                                  ↓
                            Settlement
```

1. **Order Submission** — Trader sends order via broker API (see [[Order Types and Execution]])
2. **Routing** — Broker routes to best venue (see [[Smart Order Routing]])
3. **Matching** — Exchange matches buy/sell orders by price-time priority
4. **Clearing** — Clearinghouse guarantees the trade
5. **Settlement** — T+1 (equities US), T+2 (most international), instant (crypto)

## Key Market Properties for Algo Traders

### Liquidity → [[Liquidity]]
How easily you can enter/exit positions without moving the price.

### Volatility
Price fluctuation magnitude. Higher volatility = more opportunity AND more risk.
- **Historical Volatility** — Measured from past prices
- **Implied Volatility** — Derived from options prices (see [[Options Strategies for Algos]])

### Market Efficiency
- **Efficient Market Hypothesis (EMH)** — Prices reflect all available information
  - Weak form: prices reflect past trading data
  - Semi-strong: prices reflect all public information
  - Strong: prices reflect all information including insider
- Algo trading exploits **inefficiencies** — temporary deviations from fair value

### Correlation
- Assets move together or inversely (see [[Correlation and Diversification]])
- Critical for [[Pairs Trading]] and [[Portfolio Optimization]]

## Market Regimes

Markets behave differently in different conditions:

| Regime | Characteristics | Best Strategies |
|---|---|---|
| **Trending** | Strong directional moves | [[Momentum Strategies]], [[Trend Following]] |
| **Mean-Reverting** | Range-bound oscillation | [[Mean Reversion Strategies]], [[Pairs Trading]] |
| **High Volatility** | Large swings, uncertainty | [[Options Strategies for Algos]], reduced sizing |
| **Low Volatility** | Tight ranges, compression | [[Market Making Strategies]], prepare for breakout |
| **Crisis** | Correlations spike, liquidity dries up | [[Tail Risk and Black Swans]], cash |

Detecting regime changes is one of the hardest problems in quant finance → see [[Time Series Analysis]], [[Machine Learning Strategies]].

---

**Related:** [[Asset Classes]] | [[Market Participants]] | [[Market Microstructure MOC]] | [[Trading Sessions and Hours]]
