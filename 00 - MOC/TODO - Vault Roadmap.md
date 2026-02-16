# TODO — Vault Roadmap

> Ongoing list of topics to add, notes to expand, and areas to deepen. Check items off as completed.

---

## High Priority — Add Next

### New Notes to Create
- [ ] **Greeks Deep Dive** — Full derivation of Delta, Gamma, Theta, Vega, Rho with Python implementations
- [ ] **Black-Scholes Model** — Dedicated note with derivation, assumptions, limitations, extensions
- [ ] **Volatility Surface Modeling** — SABR model, SVI parameterization, local vol vs stochastic vol
- [ ] **GARCH Models** — GARCH(1,1), EGARCH, GJR-GARCH for volatility forecasting
- [ ] **Copulas** — Dependency modeling beyond correlation, tail dependence
- [ ] **Signal Decay Analysis** — How to measure and monitor alpha decay in production
- [ ] **Risk Parity Deep Dive** — Bridgewater's All Weather, implementation details, leverage
- [ ] **Transaction Cost Models** — Almgren-Chriss detailed implementation, market impact estimation
- [ ] **Order Flow Analysis** — VPIN, order flow toxicity, information content of trades

### Expand Existing Notes
- [ ] **Supervised Learning** — Add more code examples, feature importance methods, purged CV
- [ ] **Unsupervised Learning** — K-means for regime clustering, PCA for returns
- [ ] **Reinforcement Learning** — DQN for portfolio management, policy gradient for execution
- [ ] **Natural Language Processing (NLP)** — FinBERT implementation, SEC filing parsing, earnings call analysis
- [ ] **Trend Following** — Expand with full implementation, managed futures context
- [ ] **Breakout Strategies** — Expand with Donchian channels, ATR-based breakouts
- [ ] **Options Strategies for Algos** — Expand with delta-neutral strategies, vol arb
- [ ] **Sentiment-Based Strategies** — Expand with Twitter/Reddit sentiment pipeline

---

## Medium Priority — Build Out

### New Sections
- [ ] **Fixed Income** — Bond math, yield curve, duration/convexity, rate models (Vasicek, CIR, HJM)
- [ ] **Derivatives Pricing** — Binomial trees, finite difference, Monte Carlo pricing
- [ ] **FX Trading** — Carry trade, PPP, interest rate parity, central bank analysis
- [ ] **Commodities** — Roll yield, storage theory, seasonal patterns
- [ ] **Event-Driven Strategies** — Earnings, M&A arb, index rebalancing, corporate actions

### Infrastructure Deep Dives
- [ ] **kdb+/q** — The industry-standard time-series database
- [ ] **FIX Protocol** — Message format, session management, execution reports
- [ ] **Low-Latency Optimization** — Kernel bypass, FPGA, CPU pinning, NUMA
- [ ] **Co-location** — Exchange co-lo, proximity hosting, microwave networks
- [ ] **Monitoring and Alerting** — Real-time P&L dashboards, risk dashboards

### Data Engineering
- [ ] **Tick Data Storage** — Parquet, Arctic, TimescaleDB benchmarks
- [ ] **Alternative Data Vendors** — Quandl, Refinitiv, Bloomberg, satellite data providers
- [ ] **Web Scraping for Finance** — SEC EDGAR, earnings transcripts, news

---

## Low Priority — Future Expansion

### Advanced Topics
- [ ] **Optimal Stopping Theory** — When to exit positions mathematically
- [ ] **Market Games and Mechanism Design** — Game theory in trading
- [ ] **Information Theory in Finance** — Entropy, mutual information for feature selection
- [ ] **Bayesian Portfolio Optimization** — Full Bayesian treatment beyond Black-Litterman
- [ ] **Levy Processes** — Jump-diffusion models for fat tails
- [ ] **Rough Volatility** — Fractional Brownian motion for vol modeling
- [ ] **Graph Neural Networks** — For correlation structure and supply chain analysis
- [ ] **Causal Inference** — Distinguishing correlation from causation in alpha signals

### Career & Practice
- [ ] **Quant Interview Prep** — Brain teasers, probability, coding questions
- [ ] **Strategy Pitchbook Template** — How to present a strategy to a PM/risk committee
- [ ] **Live Trading Checklist** — Pre-deployment checklist for going live
- [ ] **Post-Mortem Template** — How to analyze strategy failures

### Python Code to Add
- [ ] **Full Backtesting Engine** — Event-driven engine from scratch
- [ ] **Live Trading Bot Template** — Alpaca/IB integration with risk controls
- [ ] **Factor Model Implementation** — Fama-French 5-factor replication
- [ ] **Volatility Surface Fitter** — SVI calibration from market quotes
- [ ] **Order Book Simulator** — Simulate limit order book for market making research

---

## Completed Sections (for reference)
- [x] Foundations (01) — 7 notes
- [x] Market Microstructure (02) — 7 notes
- [x] Mathematics (03) — 10 notes (added Cointegration, Regime Detection)
- [x] Data Engineering (04) — 7 notes
- [x] Strategies (05) — 16 notes (added Alpha Research, Factor Investing, Volatility Trading)
- [x] Risk Management (06) — 8 notes
- [x] Execution (07) — 11 notes
- [x] Backtesting (08) — 8 notes
- [x] Infrastructure (09) — 5 notes
- [x] Portfolio Management (10) — 7 notes (NEW: MPT, BL, Factors, Optimization, Rebalancing, Attribution)
- [x] ML and AI (11) — 6 notes (expanded Deep Learning, ML MOC)
- [x] Regulation (12) — 7 notes (NEW: full section)
- [x] Python Code (13) — 1 note (expanded with library reference)
- [x] Resources (14) — 5 notes (NEW: Books, Papers, People, Glossary)

---

## Notes on Maintenance
- **Review quarterly:** Check for outdated information, especially regulation and technology
- **Add code as you build:** When you implement something, add the code to the relevant note
- **Link aggressively:** Every new note should link to at least 3 existing notes
- **Capture market events:** When interesting market events happen (flash crashes, regime changes), add case studies

---

**Related:** [[Trading Algorithms Master Index]] | [[Resources MOC]]
