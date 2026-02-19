# Co-location and Proximity Hosting

In the world of high-frequency trading (HFT) and ultra-low latency execution, physical distance is a significant bottleneck. **Co-location** is the practice of placing your trading servers in the same data center as the exchange's matching engine to minimize the time it takes for data to travel between them.

---

## 1. The Physics of Latency

The speed of light in a vacuum is approximately $299,792$ km/s. In fiber optic cable, it is roughly $2/3$ of that ($~200,000$ km/s).
- **1 km of fiber = 5 microseconds ($\mu s$) of one-way latency.**
- For HFT, where every microsecond matters, being 10 km away is an insurmountable disadvantage compared to being in the same building.

---

## 2. Key Exchange Data Centers (Tier-1)

| Exchange | Location | Data Center Provider |
|----------|----------|----------------------|
| **NYSE** | Mahwah, NJ | ICE (Self-managed) |
| **NASDAQ** | Carteret, NJ | Equinix NY11 |
| **CBOE / BATS** | Secaucus, NJ | Equinix NY4 |
| **CME** | Aurora, IL | CyrusOne |
| **LSE** | London, UK | Equinix LD4 / Slough |
| **Eurex / DB** | Frankfurt, DE | Equinix FR2 |
| **JPX** | Tokyo, JP | @Tokyo |

---

## 3. Connectivity Types

### A. Cross-Connects (Internal)
The fastest form of connectivity. A physical fiber optic cable run from your server rack to the exchange's "Meet-Me Room" (MMR).
- **Latency:** Nanoseconds to low microseconds.
- **Cost:** High monthly recurring fee per cable.

### B. Proximity Hosting (External)
Renting space in a data center *near* the exchange if you cannot get directly inside.
- **Example:** Hosting in Equinix NY4 to trade on NYSE (Mahwah) and NASDAQ (Carteret). The "NJ Triangle."

### C. Microwave & Millimeter Wave
For connecting different data centers (e.g., Chicago CME to NJ NYSE).
- **Logic:** Microwaves travel through air at near the speed of light, while fiber signals are slowed by glass and zig-zag paths.
- **Latency:** ~4.0 ms (Microwave) vs ~6.5 ms (Fiber) for NY-Chicago.

---

## 4. Hardware Optimization in Co-lo

Being in the building isn't enough; you must optimize the "Last Inch":
- **Fiber Spooling:** Exchanges often "equalize" cable lengths for all co-located clients so no one gets a "better" rack position.
- **Kernel Bypass:** Using NICs (like Solarflare) that send data directly to the application, bypassing the OS kernel.
- **FPGA (Field Programmable Gate Arrays):** Processing market data and making decisions in hardware (nanoseconds) rather than software (microseconds).

---

## 5. Why It Matters for Quants

1.  **Passive Fill Rates:** If you are faster, you are higher in the FIFO queue at the exchange.
2.  **Adverse Selection:** Speed allows you to cancel your quotes *before* a toxic order hits them (see [[Order Flow Analysis]]).
3.  **Latency Arbitrage:** Spotting price changes on one exchange and acting on another before the rest of the market (see [[High-Frequency Trading]]).

---

## Related Notes
- [[High-Frequency Trading Infrastructure]] — The tech stack
- [[Connectivity]] — Network protocols
- [[Trading Servers]] — Hardware optimization
- [[Order Book Dynamics]] — Queue priority
- [[Low-Latency Systems]] — (To be created) Software side
