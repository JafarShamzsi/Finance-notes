# Real-Time Data Pipelines

In algorithmic trading, a real-time data pipeline is the nervous system of the strategy. It must handle ingestion from multiple exchanges, normalize the data, and deliver it to the strategy engine with microsecond-to-millisecond latency.

---

## 1. Pipeline Architecture (Kappa/Lambda)

| Component | Function | Technology |
|-----------|----------|------------|
| **Ingestion** | Connecting to WS/REST feeds, UDP multicast. | Python (Aiohttp), C++ (Boost.Asio), Java. |
| **Normalization** | Converting vendor-specific JSON/Binary to a standard internal Schema. | Kafka, Protobuf, Avro. |
| **Stream Processing** | Calculating rolling indicators (RSI, Vol) on-the-fly. | Flink, Spark Streaming, kdb+/q. |
| **Strategy Engine** | Consuming normalized ticks to generate orders. | C++, Rust (Low-latency), Python (Low-frequency). |

---

## 2. Ingestion Challenges

### Latency vs. Throughput
- **REST Polling:** High latency, low throughput (avoid for live trading).
- **WebSockets (TCP):** Moderate latency, good throughput.
- **UDP Multicast:** Lowest latency, but requires specialized hardware (Co-lo) and handles packet loss manually.

### Normalization & Schema Registry
Data from Binance, Coinbase, and ICE all look different.
- **Protobuf/gRPC:** High-performance, binary serialization that is much faster than JSON.
- **Schema Evolution:** Handling when an exchange adds a new field to their order book message.

---

## 3. Technology Deep Dive: Apache Kafka

The standard backbone for decoupling data sources from consumers.
- **Topics:** `market_data_l2_ethusd`.
- **Partitions:** Parallelizing processing across multiple servers.
- **Zero-Copy:** Extremely high throughput by bypassing kernel-level copying.

---

## 4. Stream Processing: Apache Flink

Ideal for complex event processing (CEP).
- **Windowing:** Calculating a 5-minute VWAP using sliding windows.
- **State Management:** Tracking the current position and P&L in memory.
- **Watermarking:** Handling out-of-order ticks due to network jitter.

---

## 5. Live-to-Storage: The "Tick Sink"

Writing data to the database while simultaneously feeding the strategy.
- **Write-Ahead Logging (WAL):** Ensuring data is safe before confirming it.
- **Batching:** Accumulating ticks in memory and writing to disk in blocks (crucial for HDD/SSD performance).

---

## 6. Real-Time Quality Control

- **Gap Detection:** Identifying when a heartbeat is missed.
- **Stale Data Alerting:** Flagging if a price hasn't updated in $X$ seconds.
- **Cross-Source Validation:** Comparing prices from two different exchanges to identify outliers or exchange-specific issues.

---

## Related Notes
- [[Data Engineering MOC]] — Parent section
- [[Market Data Sources]] — Where the data starts
- [[Infrastructure MOC]] — Connectivity and servers
- [[Database Design for Trading]] — Where the pipeline ends
- [[High-Frequency Trading Infrastructure]] — The low-latency extreme
