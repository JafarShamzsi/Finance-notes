# Trading Servers

A **Trading Server** is a specialized, high-performance computer designed to host the strategy engine, risk controls, and execution gateways. Unlike general-purpose cloud servers, trading servers are tuned for deterministic performance and minimum latency.

---

## 1. Hardware Selection

### A. CPU (The Brain)
- **High Clock Speed:** For single-threaded trading logic, a higher GHz (e.g., 5.0GHz+) is more important than a high core count.
- **Cache Size:** Larger L3 cache reduces the time spent waiting for data from the RAM.
- **Architectures:** Intel Xeon or AMD EPYC are standard, but custom-overclocked Core i9s are used in some HFT shops.

### B. RAM (Memory)
- **ECC RAM:** Error Correction Code memory is essential to prevent system crashes due to bit-flips.
- **Latency over Capacity:** Trading servers typically don't need terabytes of RAM, but they need the fastest possible timing (low CAS latency).

### C. NIC (Network Interface Card)
- **HFT Grade:** Solarflare, Mellanox, or Exablaze.
- **Features:** Hardware-level timestamping and Kernel Bypass support (see [[High-Frequency Trading Infrastructure]]).

---

## 2. Operating System Optimization (Linux)

Linux is the industry standard for trading servers. To make it "Trading Ready," quants apply the following tunings:

- **RT (Real-Time) Kernel Patch:** Minimizes OS-level interruptions.
- **CPU Isolation:** Telling the OS *never* to schedule general tasks on specific cores (`isolcpus`).
- **Tickless Mode:** Disabling the OS periodic timer interrupt to ensure the CPU core is 100% dedicated to the trading code.
- **Transparent Huge Pages:** Disabling this to prevent unpredictable memory management pauses.

---

## 3. Storage and Logging

- **NVMe SSDs:** For high-speed writing of tick-by-tick market data (see [[Database Design for Trading]]).
- **Sequential Logging:** Ensuring that logging system events does not block the "Hot Path." Logging should be handled by a background thread or a dedicated disk.

---

## 4. Power and Reliability

- **Dual Power Supplies (PSU):** Connected to different power circuits.
- **UPS (Uninterruptible Power Supply):** To prevent sudden shutdowns during power flickers.
- **Environmental Control:** Trading servers generate extreme heat (especially when overclocked) and require industrial-grade cooling.

---

## 5. Deployment Architecture

| Tier | Function | Hardware |
|------|----------|----------|
| **Strategy** | Executes signals. | Overclocked, Liquid-cooled (Co-lo). |
| **Research** | Backtesting, ML training. | High core count, multiple GPUs. |
| **Data Sink** | Tick recording, DB. | Large storage capacity, high I/O throughput. |

---

## Related Notes
- [[Infrastructure MOC]] — Broader context
- [[Co-location and Proximity]] — Where the server lives
- [[High-Frequency Trading Infrastructure]] — The extreme hardware end
- [[Low-Latency Systems]] — Software side of server tuning
- [[Trading System Architecture]] — Software design for the server
- [[Database Design for Trading]] — Storage considerations
