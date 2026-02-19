# TODO — Vault Roadmap

> Ongoing list of topics to add, notes to expand, and areas to deepen. Check items off as completed.

---

## High Priority — Add Next

### New Notes to Create
- [x] **Volatility Surface Modeling** — Local Vol (Dupire), Stochastic Vol (Heston), SVI/SABR parameterization
- [x] **Market Impact Models** — Almgren-Chriss, temporary vs permanent impact, decay kernels
- [x] **FX Trading** — G10 vs EM, Carry Trade, Uncovered Interest Parity, central bank intervention
- [x] **Commodities** — Term structure (contango/backwardation), seasonality, storage costs
- [x] **Hedging Strategies** — Delta-Gamma-Vega hedging, minimum variance hedging
- [x] **Correlation and Copulas** — Tail dependence, rank correlation, Gaussian vs t-Copula

### Expand Existing Notes
- [x] **Value at Risk (VaR)** — Add Expected Shortfall (CVaR), Extreme Value Theory (EVT)
- [x] **Order Book Dynamics** — Add OBI (Order Book Imbalance), micro-price, queue position
- [x] **Backtesting Framework Design** — Event-driven engine architecture, latency simulation
- [x] **ML and AI Expansion** — Supervised, Unsupervised, Deep Learning, and RL for Trading.

---

## Medium Priority — Build Out

### Infrastructure Deep Dives
- [ ] **Low-Latency Optimization** — Kernel bypass (DPDK), FPGA, CPU pinning, lock-free queues
- [ ] **FIX Protocol** — Message types (NewOrderSingle, ExecutionReport), session layer
- [ ] **Market Data Feeds** — L1 vs L2 vs L3 data, normalization, packet loss handling

### New Sections
- [x] **Fixed Income** — Expanded bond math, yield curve modeling (Nelson-Siegel), added rate models
- [x] **Interest Rate Models** — Detailed note on Vasicek, CIR, Hull-White, HJM
- [x] **Event-Driven Strategies** — Merger arb, index rebalancing, corporate actions
- [x] **Derivatives Pricing** — Binomial trees, finite difference, Monte Carlo pricing
- [x] **FX Trading** — Carry trade, PPP, interest rate parity, central bank analysis
- [x] **Commodities** — Roll yield, storage theory, seasonal patterns

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
