# Cloud vs. On-Premise Infrastructure

Selecting the right environment for your trading stack is a fundamental decision that balances **latency**, **control**, and **cost**. Institutional quant firms typically use a hybrid approach, using on-premise hardware for execution and cloud for research.

---

## 1. On-Premise (Exchange Co-location)

Physical servers owned or leased by the firm, located inside the exchange's data center (see [[Co-location and Proximity]]).

| Factor | Detail |
|-------|--------|
| **Latency** | **Microseconds.** The fastest possible path to the matching engine. |
| **Control** | Full control over hardware (CPU overclocking, FPGA, custom NICs). |
| **Cost** | High Capex (buying hardware) and High Opex (rack space, cooling, cross-connects). |
| **Best For** | HFT, Market Making, High-Frequency Stat Arb. |

---

## 2. Cloud Infrastructure (AWS, Azure, GCP)

Virtual servers and services provided by major tech vendors.

| Factor | Detail |
|-------|--------|
| **Latency** | **Milliseconds.** Variable and subject to "noisy neighbors" (jitter). |
| **Scalability** | Spin up 1,000 servers for a backtest in seconds and shut them down when done. |
| **Cost** | No Capex. Pay-as-you-go. Can be expensive for continuous heavy compute. |
| **Best For** | ML Training, Large-scale Backtesting, Low-frequency strategies (Daily/Weekly). |

---

## 3. Comparison Matrix

| Feature | On-Premise (Co-lo) | Public Cloud |
|---------|-------------------|--------------|
| **Deterministic Performance** | Excellent (fixed hardware). | Poor (hypervisor overhead). |
| **Market Data Access** | Direct multicast feeds. | Usually via unicast proxy (delayed). |
| **Security** | Maximum (Air-gapped possible). | High, but shared responsibility. |
| **Time-to-Market** | Weeks/Months (shipping hardware). | Minutes (API call). |
| **FPGA Support** | Native. | Limited (e.g., AWS F1). |

---

## 4. The Hybrid Quant Architecture

Modern mid-to-large size quant funds typically build this "Best of Both Worlds" architecture:

1.  **Execution Edge (On-Prem):** Small clusters of high-performance servers in NJ, Chicago, London, and Tokyo for low-latency order firing.
2.  **Data Lake (Cloud/On-Prem):** Large-scale storage for decades of tick data.
3.  **Research Engine (Cloud):** Using spot instances or GPU clusters to train deep learning models and run massive [[Walk-Forward Analysis]] simulations.

---

## 5. Connectivity Considerations

Even if your strategy is in the cloud, you may need a **Leased Line** (Extranet) to the exchange to get a reliable market data feed, as the public internet is too unstable for production trading.

---

## Related Notes
- [[Infrastructure MOC]] — System context
- [[Co-location and Proximity]] — The on-premise extreme
- [[Trading Servers]] — Hardware optimization
- [[Connectivity]] — Networking the environment
- [[Trading System Architecture]] — Designing for the environment
- [[Backtesting Platforms and Frameworks]] — Cloud-based backtesting (QuantConnect)
