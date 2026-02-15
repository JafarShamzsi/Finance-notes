# Asset Classes

An **asset class** is a group of financial instruments with similar characteristics and behavior. Each has unique properties that affect how algorithms should trade them.

---

## Equities (Stocks)

**What:** Ownership shares in public companies.

| Property | Detail |
|---|---|
| Trading Hours | 9:30-16:00 ET (US), pre/post-market available |
| Settlement | T+1 (US) |
| Tick Size | $0.01 |
| Key Data | Price, volume, fundamentals, earnings |
| Regulation | SEC, FINRA (see [[SEC and FINRA Regulations]]) |

**Algo Opportunities:**
- [[Momentum Strategies]] around earnings announcements
- [[Mean Reversion Strategies]] on intraday overreactions
- [[Statistical Arbitrage]] across correlated stocks
- [[Pairs Trading]] within sectors

**Key Indices:** S&P 500, NASDAQ 100, Russell 2000, DJIA

---

## Fixed Income (Bonds)

**What:** Debt instruments — you lend money, receive interest.

| Property | Detail |
|---|---|
| Types | Government (Treasuries), Corporate, Municipal |
| Key Metrics | Yield, Duration, Convexity, Credit Spread |
| Market | Mostly OTC |
| Drivers | Interest rates, inflation, credit risk |

**Algo Opportunities:**
- Yield curve trading
- Credit spread arbitrage
- Duration-neutral strategies
- Treasury basis trades

---

## Foreign Exchange (Forex/FX)

**What:** Trading currency pairs (EUR/USD, GBP/JPY, etc.)

| Property | Detail |
|---|---|
| Market Size | ~$7.5 trillion daily volume |
| Hours | 24 hours, Sunday 17:00 ET - Friday 17:00 ET |
| Structure | Decentralized interbank + retail ECN |
| Leverage | Up to 50:1 (US), 500:1 (offshore) |
| Costs | Spread-based, no commission on most pairs |

**Algo Opportunities:**
- [[Trend Following]] on macro trends
- Carry trade (borrow low-yield, invest high-yield)
- Triangular arbitrage (3-currency mispricings)
- News-based high-frequency strategies

**Major Pairs:** EUR/USD, USD/JPY, GBP/USD, USD/CHF
**Crosses:** EUR/GBP, AUD/NZD, EUR/JPY

---

## Commodities

**What:** Raw materials and agricultural products.

| Category | Examples |
|---|---|
| Energy | Crude Oil (WTI, Brent), Natural Gas |
| Metals | Gold, Silver, Copper, Platinum |
| Agriculture | Corn, Wheat, Soybeans, Coffee |
| Livestock | Cattle, Hogs |

Traded primarily via **futures contracts** on CME, ICE, LME.

**Algo Opportunities:**
- Seasonal patterns (agriculture, natural gas)
- Contango/backwardation roll strategies
- Cross-commodity spread trading
- Macro-driven [[Trend Following]]

---

## Derivatives

### Futures
Standardized contracts to buy/sell at a future date and price.
- Used for hedging and speculation
- **Margin-based** — only deposit a fraction of notional value
- Key products: ES (S&P 500), NQ (NASDAQ), CL (Crude), ZB (Bonds)

### Options
Right (not obligation) to buy (call) or sell (put) at a strike price.
- Greeks: Delta (Δ), Gamma (Γ), Theta (Θ), Vega (ν), Rho (ρ)
- See [[Options Strategies for Algos]] for detailed algo applications
- Volatility surface trading, delta hedging

### Swaps
OTC contracts to exchange cash flows. Interest rate swaps, credit default swaps.

---

## Cryptocurrencies

**What:** Digital assets on blockchain networks.

| Property | Detail |
|---|---|
| Hours | 24/7/365 |
| Settlement | Near-instant on-chain |
| Exchanges | Binance, Coinbase, Kraken, Bybit |
| Volatility | Very high (annualized 60-100%+) |
| Regulation | Evolving rapidly |

**Algo Opportunities:**
- [[Crypto Algorithmic Trading]] — unique market structure
- Cross-exchange arbitrage (CEX ↔ CEX, CEX ↔ DEX)
- Funding rate arbitrage (perp vs spot)
- DeFi yield farming automation
- [[Momentum Strategies]] — stronger trends due to retail-dominated market

---

## Asset Class Comparison for Algo Trading

| Factor | Equities | FX | Futures | Crypto |
|---|---|---|---|---|
| Data availability | Excellent | Good | Good | Excellent |
| Liquidity | High (large caps) | Very High | High | Variable |
| Transaction costs | Low | Very Low | Low | Medium |
| Leverage | 2-4x (retail) | 50-500x | 10-20x | 1-100x |
| Hours | Limited | 24/5 | Extended | 24/7 |
| Algo competition | Very High | High | High | Medium |
| Barrier to entry | Low | Low | Medium | Low |

---

**Related:** [[Financial Markets Overview]] | [[Order Types and Execution]] | [[Market Participants]] | [[Fees Commissions and Slippage]]
