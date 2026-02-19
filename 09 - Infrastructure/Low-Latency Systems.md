# Low-Latency Systems

Low-latency engineering is the art of minimizing the time between receiving a market event and reacting to it. In HFT, this latency is measured in **microseconds ($\mu s$)** or even **nanoseconds ($ns$)**.

---

## 1. Sources of Software Latency

To build a fast system, you must eliminate the following bottlenecks:

### A. Context Switching
When the OS moves a process from one CPU core to another.
- **Solution:** **CPU Pinning (Affinity)**. Force the strategy thread to stay on a dedicated core.

### B. Garbage Collection (GC)
In languages like Java or C#, the system "pauses" to clean up memory.
- **Solution:** Avoid object allocation in the "Hot Path." Use object pools or move to **C++ / Rust**.

### C. Kernel Overhead
The standard Linux networking stack is designed for general use, not speed.
- **Solution:** **Kernel Bypass**. Use libraries like **DPDK** or **Solarflare's Onload** to read data directly from the Network Card (NIC) into the application memory.

---

## 2. Low-Latency Programming Patterns

### A. Lock-Free Data Structures
Standard locks (mutexes) are slow.
- **Solution:** Use **Atomic Operations** and **Single-Producer / Single-Consumer (SPSC)** queues (like the LMAX Disruptor pattern).

### B. Cache Locality
CPUs are much faster than RAM.
- **Solution:** Organize data in memory so it fits in the **L1/L2 Cache**. Use **Data Oriented Design** (Arrays of structures vs. Structures of arrays).

### C. Branch Prediction Optimization
Help the CPU guess the next instruction.
- **Solution:** Minimize `if/else` logic in the hot path. Use `likely()` and `unlikely()` macros in C++.

---

## 3. Hardware Acceleration (FPGA)

**FPGA (Field Programmable Gate Arrays)** are chips where the logic is burned into the hardware.
- **Speed:** $Tick 	o Trade$ in < 500 nanoseconds.
- **Use Case:** Market data parsing, simple risk checks, and order firing.

---

## 4. Measuring Latency

You cannot improve what you do not measure.
- **Wire-to-Wire Latency:** Time from packet hitting the NIC to packet leaving the NIC.
- **Tick-to-Trade Latency:** Internal software processing time.
- **Tooling:** Use hardware timestamps (PTP - Precision Time Protocol) for microsecond accuracy across different servers.

---

## 5. The Tradeoff: Speed vs. Complexity

| Speed | Language / Tech | Development Time | Flexibility |
|-------|-----------------|------------------|-------------|
| **Slow** (1ms+) | Python | Fast | Very High |
| **Medium** (100$\mu s$) | Java / C# | Medium | High |
| **Fast** (10$\mu s$) | C++ / Rust | Slow | Medium |
| **Ultra-Fast** (<1$\mu s$) | FPGA (Verilog) | Very Slow | Low |

---

## Related Notes
- [[High-Frequency Trading Infrastructure]] — The hardware side
- [[Co-location and Proximity]] — Reducing distance
- [[Trading System Architecture]] — Designing for speed
- [[FIX Protocol]] — The communication overhead
- [[Connectivity]] — Network layer
