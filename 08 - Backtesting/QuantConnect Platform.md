# QuantConnect Platform

**QuantConnect** is a leading cloud-based algorithmic trading platform that provides an institutional-grade environment for designing, testing, and deploying trading strategies across multiple asset classes (Equities, Forex, Futures, Options, and Crypto).

---

## 1. The LEAN Engine

At the heart of QuantConnect is the **LEAN Algorithm Framework**, an open-source, event-driven backtesting engine written in C#.
- **Multi-Language Support:** Write strategies in **Python** or **C#**.
- **Event-Driven:** Mimics live trading by processing data tick-by-tick or bar-by-bar.
- **Cross-Platform:** Can be run locally via Docker or in the QuantConnect cloud.

---

## 2. Key Features for Quants

### A. Integrated Data Feed
QuantConnect provides access to terabytes of historical data, including:
- **US Equities:** SIP tick data since 1998 (survivorship-bias free).
- **Options:** Full OPRA chain data.
- **Alternative Data:** News sentiment, corporate filings, and more.

### B. Cloud Computing & Optimization
- **Parallel Backtesting:** Run hundreds of backtests simultaneously.
- **Optimization:** Built-in tools for parameter tuning using genetic algorithms or grid search (be careful of [[Overfitting]]).

### C. Live Trading Deployment
Seamlessly transition from backtest to live trading with integrated brokers:
- Interactive Brokers (IBKR)
- Tradier
- OANDA
- Coinbase / Binance

---

## 3. The LEAN Framework Architecture

A QuantConnect algorithm typically follows this structure:

```python
class MyAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100000)
        # Add assets
        self.symbol = self.AddEquity("AAPL", Resolution.Minute).Symbol
        # Define Universe, Alpha, Portfolio, Execution, and Risk models

    def OnData(self, data):
        # Event handler for new market data
        if not self.Portfolio.Invested:
            self.SetHoldings(self.symbol, 1.0)
```

---

## 4. Pros and Cons

| Pros | Cons |
|------|------|
| Massive data library included. | Learning curve for the LEAN framework. |
| Eliminates infrastructure "plumbing" work. | Cloud latency might be too high for HFT. |
| Survivorship-bias free equity data. | Debugging cloud backtests can be slow. |
| Open-source engine (LEAN). | Subscription cost for high-end features. |

---

## 5. Local Development vs. Cloud

- **Cloud:** Easy access to data and compute; good for most strategies.
- **Local (Lean CLI):** Better for proprietary data, custom libraries, and integration with local ML pipelines (PyTorch/TensorFlow).

---

## Related Notes
- [[Backtesting Platforms and Frameworks]] — Comparison
- [[Backtesting Framework Design]] — Underlying logic
- [[Market Data Sources]] — Where QC gets its data
- [[Python Code MOC]] — Using Python in LEAN
