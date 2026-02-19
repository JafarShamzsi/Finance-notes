# Connectivity

In algorithmic trading, **Connectivity** refers to the physical and logical links between a trading system and the execution venues. For low-latency strategies, connectivity is often the single most expensive and critical part of the infrastructure.

---

## 1. The Connectivity Hierarchy

| Level | Type | Latency | Cost | Use Case |
|-------|------|---------|------|----------|
| **1** | **Cross-Connect** | < 1 $\mu s$ | Very High | HFT, Market Making (Co-lo). |
| **2** | **Leased Line (Extranet)** | 1-10 $ms$ | High | Institutional Execution, SOR. |
| **3** | **VPN (Public Internet)** | 20-100 $ms$ | Medium | Retail Algos, Backtesting. |
| **4** | **Standard Internet** | 50+ $ms$ | Low | Data research, general access. |

---

## 2. Protocols: Text vs. Binary

How the system actually speaks to the exchange.

### A. FIX Protocol (Financial Information eXchange)
The industry standard for order submission and management.
- **Format:** Tag-value text (e.g., `35=D|44=150.00`).
- **Pros:** Universal, human-readable, easy to debug.
- **Cons:** Slow to parse (relative to binary).
- See [[FIX Protocol]] for details.

### B. Binary / Native Protocols
Used by exchanges for their fastest data feeds and execution gateways.
- **Examples:** ITCH (NASDAQ), SBE (Simple Binary Encoding - CME).
- **Pros:** Extremely low parsing overhead, compact message size.
- **Cons:** Proprietary, harder to implement.

---

## 3. Network Jitter & Packet Loss

It's not just about "Average Latency"; it's about **Consistency**.

- **Jitter:** Variation in latency over time. A strategy that expects 5ms but occasionally gets 50ms will miss opportunities or get bad fills.
- **Packet Loss:** In UDP-based market data feeds, a lost packet means missing a price update. Systems must use sequence numbers to detect and recover gaps.

---

## 4. Redundancy & Path Diversity

Production systems require multiple paths to the exchange to prevent a "Single Point of Failure."
- **Primary/Secondary Links:** Different providers (e.g., Verizon and AT&T) using different physical routes to the same building.
- **Failover Logic:** If the primary FIX session drops, the system must instantly re-establish on the secondary line.

---

## 5. Wireless Connectivity (Microwave)

For connecting distant markets (e.g., Chicago CME to New Jersey NYSE).
- **Why:** Microwaves travel through air at near the speed of light ($c$), whereas signals in fiber optic glass are slowed down by ~30%.
- **Latency Advantage:** Saving ~2 milliseconds on a NY-Chicago round trip.

---

## Related Notes
- [[Infrastructure MOC]] — Broader system design
- [[Co-location and Proximity]] — Physical aspects
- [[FIX Protocol]] — Logical messaging layer
- [[Trading Servers]] — Connecting servers to the network
- [[Low-Latency Systems]] — Software optimizations for connectivity
- [[High-Frequency Trading Infrastructure]] — The low-latency extreme
