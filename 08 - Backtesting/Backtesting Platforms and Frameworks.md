# Backtesting Platforms and Frameworks

Choosing the right backtesting platform depends on your strategy's complexity, data needs, and performance requirements. Quants generally choose between **Vectorized** (fast, simple) and **Event-Driven** (realistic, complex) frameworks.

---

## 1. Classification of Frameworks

### A. Vectorized Frameworks
Treat data as large matrices. Extremely fast for simple signals.
- **Tools:** **VectorBT**, Pandas/NumPy.
- **Best For:** Technical indicators, simple long/short signals on OHLCV data.

### B. Event-Driven Frameworks
Mimics real-world trading by iterating through time steps (ticks/bars) and processing events.
- **Tools:** **LEAN**, **Backtrader**, **Zipline**, **NautilusTrader**.
- **Best For:** High-frequency, multi-asset, complex order types, and realistic execution simulation.

---

## 2. Top Platforms for Quants

| Platform | Type | Language | Best For |
|----------|------|----------|----------|
| **QuantConnect** | Cloud/LEAN | Python / C# | Multi-asset institutional research. See [[QuantConnect Platform]]. |
| **VectorBT** | Vectorized | Python | Fast hyperparameter optimization. |
| **Backtrader** | Event-Driven | Python | Retail-friendly, highly flexible. |
| **Zipline** | Event-Driven | Python | Large-scale equity research (legacy standard). |
| **Lean (Local)** | Event-Driven | C# / Python | Proprietary local data and custom ML integration. |
| **NautilusTrader** | Event-Driven | Rust / Python | High-performance, low-latency HFT research. |

---

## 3. Cloud vs. Local Solutions

### Cloud (QuantConnect, Blueshift)
- **Pros:** Integrated data, no infrastructure setup, easy backtest sharing.
- **Cons:** Data privacy concerns, latency, subscription costs.

### Local (Lean CLI, VectorBT, Custom)
- **Pros:** Full control over data, no costs, privacy, integration with local ML GPUs.
- **Cons:** You must manage the data pipelines, hardware, and backup.

---

## 4. Key Evaluation Criteria

1.  **Execution Realism:** Does it support [[Market Impact Models]] and [[Slippage]]?
2.  **Data Quality:** Is the provided data adjusted for splits and dividends? Does it have [[Survivorship Bias]]?
3.  **Broker Integration:** Can you deploy the exact same code to live trading (e.g., IBKR, Binance)?
4.  **Community/Docs:** How easy is it to find help when you hit a bug?

---

## 5. Decision Matrix

- **"I want to test 10,000 parameter combinations in 10 seconds":** Use **VectorBT**.
- **"I want to test a complex pairs trading strategy with limit orders":** Use **Backtrader** or **LEAN**.
- **"I need survivorship-bias free data and don't want to buy it":** Use **QuantConnect**.
- **"I am building an HFT strategy that requires nanosecond precision":** Build a custom **C++** engine.

---

## Related Notes
- [[Backtesting Framework Design]] — Underlying logic
- [[QuantConnect Platform]] — Deep dive on QC
- [[Python Code MOC]] — Libraries used
- [[Market Data Sources]] — Where to get your own data
- [[Walk-Forward Analysis]] — Validation method
