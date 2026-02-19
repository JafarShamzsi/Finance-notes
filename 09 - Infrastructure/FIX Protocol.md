# FIX Protocol (Financial Information eXchange)

The **FIX Protocol** is the industry standard for real-time electronic communication between financial institutions (Brokers, Buy-side firms, Exchanges). It is a tag-value based messaging protocol that handles order submission, market data, and trade reporting.

---

## 1. Message Structure

A FIX message is a series of key-value pairs separated by a delimiter (ASCII 01 - SOH).
`Tag=Value|Tag=Value|...`

**Common Tags:**
- `35`: Message Type (e.g., `35=D` is a New Order Single).
- `44`: Price.
- `38`: Order Quantity.
- `55`: Symbol (Ticker).
- `54`: Side (1=Buy, 2=Sell).
- `49`: SenderCompID.
- `56`: TargetCompID.

---

## 2. Session Layer vs. Application Layer

### A. Session Layer (The "Pipe")
Ensures the connection is reliable and messages are delivered in order.
- **Logon (`35=A`):** Establish connection.
- **Heartbeat (`35=0`):** Ensure the line is still alive.
- **Resend Request (`35=2`):** Request missing messages if there is a sequence number gap.

### B. Application Layer (The "Business")
The actual trading commands.
- **New Order Single (`35=D`):** Send a new buy/sell order.
- **Execution Report (`35=8`):** The broker/exchange confirms a fill, a partial fill, or a reject.
- **Order Cancel Request (`35=F`):** Request to pull an order.

---

## 3. Order Lifecycle Example

1.  **Client:** Sends `35=D` (New Order).
2.  **Broker:** Returns `35=8` (Execution Report - **Pending New**).
3.  **Broker:** Returns `35=8` (Execution Report - **New**).
4.  **Broker:** Returns `35=8` (Execution Report - **Partial Fill**).
5.  **Broker:** Returns `35=8` (Execution Report - **Filled**).

---

## 4. Performance & Binary Variants

Standard FIX is text-based and relatively slow due to parsing overhead.
- **FIX Performance:** 50$\mu s$ to 500$\mu s$ parsing time.
- **SBE (Simple Binary Encoding):** A high-performance binary version of FIX used by modern exchanges (CME, NASDAQ) to reduce latency to the low microsecond range.
- **FIX FAST:** Another compressed variant used primarily for market data.

---

## 5. Implementation for Quants

Most quants use a "FIX Engine" rather than writing the protocol from scratch.
- **QuickFIX:** The most popular open-source engine (available in C++, Python, Java).
- **Chronicle FIX:** A high-performance Java-based engine used by hedge funds.

---

## Related Notes
- [[Trading System Architecture]] — Integration of FIX
- [[Order Types and Execution]] — Business logic behind FIX
- [[Low-Latency Systems]] — Optimization of communication
- [[High-Frequency Trading Infrastructure]] — Binary protocols
- [[Connectivity]] — Underlying TCP/IP layer
