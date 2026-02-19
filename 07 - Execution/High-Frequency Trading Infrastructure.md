# High-Frequency Trading (HFT) Infrastructure

HFT infrastructure is built for one purpose: **minimizing the round-trip latency** between a market event and an execution response. In this world, edges are measured in nanoseconds, and the entire technology stack is customized for performance.

---

## 1. The Hardware Stack

### A. FPGA (Field Programmable Gate Arrays)
Hardware chips where the logic is "burned" into the circuitry.
- **Role:** Handles market data parsing and simple risk checks in < 500ns.
- **Why:** Bypasses the CPU and OS entirely.

### B. Network Interface Cards (NICs)
High-performance NICs (e.g., Solarflare, Exablaze) designed for low latency.
- **Hardware Timestamps:** Every packet is timestamped the moment it hits the wire with nanosecond precision.

### C. Overclocked Servers
Custom liquid-cooled servers with CPUs locked at high frequencies (e.g., 5.0GHz+) to minimize instruction processing time.

---

## 2. Operating System & Software Tuning

### A. Kernel Bypass
The standard Linux networking stack is too slow for HFT.
- **Solution:** Using libraries like **Solarflare Onload** or **DPDK** to move data directly from the NIC to the application's memory space, bypassing the OS kernel.

### B. CPU Pinning & Isolation
Preventing the OS from moving the trading process between different CPU cores.
- **Technique:** Dedicating specific cores strictly to the trading strategy and isolating them from all other system tasks.

### C. No Memory Allocation
In the "Hot Path" (the code that runs when a tick arrives), no new memory is allocated. This prevents "Garbage Collection" pauses or memory management overhead.

---

## 3. High-Performance Networking

- **UDP Multicast:** The standard for market data (no handshaking overhead).
- **Direct Exchange Feeds:** Bypassing consolidated tapes (like the SIP) to get data directly from the exchange matching engine.
- **Microwave Links:** Using wireless towers to send data between cities (e.g., Chicago to NY) faster than fiber optic cables (see [[Co-location and Proximity]]).

---

## 4. Latency Breakdown: Tick-to-Trade

A typical HFT "Tick-to-Trade" cycle aims for < 10 microseconds:

| Component | Latency |
|-----------|---------|
| Wire-to-NIC | ~100 $ns$ |
| Data Normalization (FPGA) | ~500 $ns$ |
| Signal Calculation | ~2 $\mu s$ |
| Pre-Trade Risk Check | ~500 $ns$ |
| Order Serialization | ~500 $ns$ |
| NIC-to-Wire | ~100 $ns$ |

---

## 5. Reliability and "Kill Switches"

Because HFT systems can send thousands of orders per second, a "bug" can bankrupt a firm in minutes (e.g., Knight Capital).
- **Hardware Kill Switch:** A physical or FPGA-level check that stops all trading if P&L or position limits are breached.
- **Throttling:** Limits on the number of messages sent per second to avoid being "banned" by the exchange.

---

## Related Notes
- [[Infrastructure MOC]] — System context
- [[Co-location and Proximity]] — Physical placement
- [[Low-Latency Systems]] — Software optimizations
- [[Connectivity]] — Network protocols
- [[Trading System Architecture]] — Designing the "Hot Path"
- [[FIX Protocol]] — Communicating with venues
