# High-Frequency Trading (HFT)

**Core Idea:** Use extreme speed and technology advantage to capture tiny, fleeting opportunities millions of times. Microsecond execution, massive volume, razor-thin margins.

---

## Characteristics

| Property | Detail |
|---|---|
| Holding period | Microseconds to minutes |
| Trades per day | 10,000 - 1,000,000+ |
| Profit per trade | $0.001 - $0.10 |
| Win rate | 51-55% |
| Capital required | $1M+ (infra costs) |
| Latency requirement | < 10 microseconds |

## HFT Strategy Types

### 1. Latency Arbitrage
Exploit speed advantage to front-run slower participants.

```
Exchange A shows: AAPL = $150.00
Exchange B still shows: AAPL = $149.98 (stale)

Action: Buy at $149.98 on B, sell at $150.00 on A
Profit: $0.02/share × 10,000 shares = $200 (in microseconds)
```

Requires: [[Co-location and Proximity]], direct market feeds, fastest hardware.

### 2. Statistical Market Making
See [[Market Making Strategies]] — but at nanosecond speed.
- Quote-stuffing prevention
- Ultra-fast inventory management
- Predictive models for next-tick price

### 3. Event-Driven HFT
React to structured data releases faster than anyone:
- Economic data (NFP, CPI, FOMC)
- Earnings (parsing 10-Q/10-K in microseconds)
- News wire parsing (NLP at speed)

### 4. Order Book Imbalance
Predict short-term price direction from [[Order Book Dynamics]]:
```
Imbalance = (Bid_Volume - Ask_Volume) / (Bid_Volume + Ask_Volume)

High imbalance → price likely moves in imbalance direction
```

### 5. Momentum Ignition (Controversial)
Place orders to trigger other algos' stop orders or momentum signals, then trade against the resulting cascade. Regulatory gray area.

## Technology Stack

```
Market Data Feed (Exchange co-lo)
        ↓ (< 1 μs)
FPGA / Kernel Bypass NIC
        ↓ (< 1 μs)
Signal Generation (C++/FPGA)
        ↓ (< 1 μs)
Risk Check (hardware)
        ↓ (< 1 μs)
Order Gateway (FIX/native protocol)
        ↓ (< 1 μs)
Exchange Matching Engine
```

### Key Technologies
| Component | Technology |
|---|---|
| Language | C++, FPGA (Verilog/VHDL) |
| Networking | Kernel bypass (DPDK, Solarflare) |
| Data feed | Direct exchange feeds (not consolidated) |
| Hardware | Custom FPGA boards, GPU acceleration |
| Location | [[Co-location and Proximity]] at exchange data center |
| OS | Custom Linux kernel, CPU pinning, NUMA-aware |

## Latency Breakdown

```
Source of latency:
  Network (co-lo to exchange):     ~1 μs
  NIC processing:                  ~1 μs
  Application logic:               ~1-5 μs
  Risk checks:                     ~1 μs
  Order serialization:             ~1 μs
  ─────────────────────────────────────
  Total tick-to-trade:             5-10 μs

Competitive edge often measured in nanoseconds.
```

## HFT Firms

| Firm | Known For |
|---|---|
| Citadel Securities | Largest US market maker |
| Virtu Financial | ~99% profitable trading days |
| Jump Trading | Microwave towers for speed |
| Tower Research | Ultra-low latency |
| Jane Street | ETF/options market making |
| Optiver | Options market making |
| IMC | Global market making |
| DRW | Diverse HFT strategies |

## HFT P&L Characteristics

```
Daily P&L distribution:
  Highly concentrated around small positive values
  Very few losing days
  Sharpe ratios: 5-20+ (annualized)
  Revenue per dollar of volume: tiny but consistent

Example (Virtu Financial public data):
  1,238 out of 1,240 trading days profitable (2009-2014)
```

## Can Retail Compete?

**Short answer: No.** Not in pure HFT.

**But you can:**
- Trade on longer timeframes where speed doesn't matter
- Use [[Statistical Arbitrage]] with holding periods of hours/days
- Exploit signals in [[Alternative Data]] that HFTs don't model
- Focus on less competitive markets ([[Crypto Algorithmic Trading]])
- Use [[Machine Learning Strategies]] on novel data sources

## Regulatory Concerns

- [[SEC and FINRA Regulations]] — Market access rules, risk controls
- [[MiFID II]] — EU regulations on algorithmic trading
- Flash Crash of 2010 — Led to circuit breakers
- Debate: Does HFT improve or harm market quality?
- Kill switch requirements
- See [[Market Manipulation Laws]]

---

**Related:** [[Market Making Strategies]] | [[Low-Latency Systems]] | [[Co-location and Proximity]] | [[Order Book Dynamics]] | [[FIX Protocol]]
