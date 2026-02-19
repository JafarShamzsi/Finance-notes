# Market Data Feeds

**Market Data Feeds** are the raw stream of information coming from financial exchanges. They provide the prices, trade reports, and order book depth that power every quantitative model.

---

## 1. Data Levels

| Level | Content | Complexity | Use Case |
|-------|---------|------------|----------|
| **L1 (Top of Book)** | Best Bid, Best Ask, and Last Trade price/size. | Low | Basic technical analysis, simple retail bots. |
| **L2 (Market Depth)** | Aggregate volume at multiple price levels (e.g., top 10 bids/asks). | Medium | Mid-frequency trading, execution algorithms. |
| **L3 (Order Detail)** | Every individual limit order in the book. | High | HFT, Market Making, detecting [[Iceberg Orders]]. |

---

## 2. Delivery Protocols: Multicast vs. Unicast

### A. UDP Multicast (The Institutional Standard)
The exchange broadcasts a single stream of data, and all participants "listen" to it simultaneously.
- **Latency:** Extremely low (no handshake).
- **Cons:** Unreliable. If a packet is dropped, it's gone forever (Gap detection/recovery required).

### B. TCP Unicast (Standard API)
A one-to-one connection between you and the data provider (e.g., WebSockets).
- **Latency:** Higher due to TCP overhead and handshaking.
- **Pros:** Reliable. The protocol ensures every packet arrives in order.

---

## 3. Direct Feeds vs. Consolidated Feeds

- **Direct Feeds:** Connecting directly to each exchange (e.g., NASDAQ TotalView). fastest, most expensive.
- **Consolidated Feed (SIP):** In the US, the SIP combines all exchange data into a single stream. cheaper but has "Consolidated Tape" latency (latency between exchange event and SIP update).

---

## 4. Normalization & Feed Handlers

Every exchange has a different message format (JSON, FIX, Binary). A **Feed Handler** is a piece of software that:
1.  **Ingests:** Receives the raw binary/text packets.
2.  **Parses:** Converts them into a standard internal format (e.g., Protobuf).
3.  **Timestamps:** Adds a high-precision timestamp the moment the packet hits the NIC.
4.  **Publishes:** Sends the normalized tick to the strategy engine via a message bus (see [[Trading System Architecture]]).

---

## 5. Data Feed Health & Monitoring

- **Stale Ticks:** Detecting if a feed has stopped updating (often a sign of exchange or network failure).
- **Sequence Gaps:** Detecting missing packets in a UDP feed and requesting re-transmission.
- **Latency Spikes:** Monitoring the time between the exchange's matching engine timestamp and your arrival timestamp.

---

## Related Notes
- [[Data Engineering MOC]] — Storage and cleaning
- [[Tick Data and Trade Data]] — The raw material
- [[Infrastructure MOC]] — System context
- [[Connectivity]] — Underlying network links
- [[Trading System Architecture]] — Where the feed is consumed
- [[High-Frequency Trading Infrastructure]] — Maximizing feed speed
