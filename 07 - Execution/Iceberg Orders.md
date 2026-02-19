# Iceberg Orders (Reserve Orders)

An **Iceberg Order** is a large limit order broken into smaller "visible" portions (the tip) and a "hidden" portion (the bulk). It is the most common way to execute large size on a public exchange without causing immediate price panic.

---

## 1. How It Works: The Peak & The Reserve

An iceberg order has two primary parameters:
- **Total Quantity:** The full order size (e.g., 10,000 shares).
- **Peak Size (Display Size):** The amount visible in the L2 book (e.g., 500 shares).

**The Refill Mechanism:**
1.  **Placement:** 500 shares are placed at the best bid. 9,500 are hidden in the exchange's matching engine.
2.  **Execution:** A seller hits the 500 shares.
3.  **Replenishment:** Once the 500 are gone, the exchange automatically places *another* 500 shares from the hidden reserve.
4.  **Repeat:** This continues until the full 10,000 shares are filled.

---

## 2. Advanced Features: Randomization

Fixed-size peaks (e.g., exactly 500 shares every time) are easily detected by HFT algorithms.
- **Randomized Peak Size:** Instead of a fixed 500, the algorithm might display 480, then 512, then 495.
- **Randomized Time Delays:** Adding a small, stochastic delay before refilling the peak to simulate a manual trader or a slower algorithm.

---

## 3. The Goal: Reducing Market Impact

By only showing a small portion, the trader avoids:
- **Quote Stuffing:** Other traders jumping ahead (pennying) if they see a massive 10,000-share buyer.
- **Panic Selling:** The market interpreting a large order as a sign of institutional selling/deleveraging.

---

## 4. Detection by HFTs (Iceberg Sniffing)

Sophisticated algorithms "sniff out" icebergs by looking for "sticky" price levels.
- **The Signal:** If a 500-share bid is hit 5 times in a row, but the size never decreases, it is almost certainly an iceberg.
- **The Reaction:** HFTs may front-run the iceberg or "probe" it with small orders to determine its true depth.

---

## 5. Iceberg vs. Hidden Orders

| Feature | Iceberg Order | Fully Hidden Order |
|---------|---------------|-------------------|
| **Visibility** | Part (the peak) is visible. | 100% invisible. |
| **Priority** | Visible part has price/time priority. | Usually has lower priority than all visible orders. |
| **Fees** | Normal exchange fees. | Often higher fees (execution premium for being hidden). |

---

## 6. Implementation Checklist for Quants

- [ ] **Venue Support:** Does the exchange support "native" iceberg orders, or must you build a synthetic one in your execution engine?
- [ ] **Peak Sizing:** Is the peak size large enough to get filled but small enough to remain stealthy? (Rule of thumb: < 5% of average L1 size).
- [ ] **Anti-Gaming:** Are you using enough randomization to prevent HFT detection?

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[Order Book Dynamics]] — Interaction with L2 data
- [[Market Impact Models]] — Why we use icebergs
- [[VWAP Algorithm]] — Using icebergs as an execution strategy
- [[High-Frequency Trading]] — The "sniffers"
