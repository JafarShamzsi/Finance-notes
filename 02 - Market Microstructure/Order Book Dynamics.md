# Order Book Dynamics

The order book is the central data structure of electronic markets. Understanding it is essential for every algorithmic trader.

---

## Structure

```
         ASK (Sellers)
    ┌─────────────────────┐
    │ $100.05  ×  500     │  Level 3
    │ $100.04  ×  1,200   │  Level 2
    │ $100.03  ×  3,000   │  Level 1 (Best Ask)
    ├─────────────────────┤  ← Spread ($0.02)
    │ $100.01  ×  2,500   │  Level 1 (Best Bid)
    │ $100.00  ×  800     │  Level 2
    │ $99.99   ×  1,500   │  Level 3
    └─────────────────────┘
         BID (Buyers)

Mid Price = ($100.01 + $100.03) / 2 = $100.02
Spread = $100.03 - $100.01 = $0.02
```

## Data Levels

| Level | Contains | Use |
|---|---|---|
| **L1** | Best bid/ask (NBBO) | Basic strategies |
| **L2** | Multiple price levels with aggregate size | Most algo trading |
| **L3** | Individual orders at each level | HFT, market making |

## Key Metrics

### Order Book Imbalance (OBI)
Predictive of short-term price direction. A surplus of bid volume suggests buying pressure.

$$ \text{OBI} = \frac{V_b - V_a}{V_b + V_a} $$

- **Research:** Cont et al. (2014) showed OBI is the single strongest predictor of the next tick direction.

```python
def order_book_imbalance(bid_volume, ask_volume):
    """
    Predictive of short-term price direction.
    +1 = all bids (bullish), -1 = all asks (bearish)
    """
    return (bid_volume - ask_volume) / (bid_volume + ask_volume)
```

### Micro-Price (Volume-Weighted Mid Price)
The mid-price assumes the next trade is equally likely to be a buy or sell. The micro-price adjusts for the imbalance.

$$ P_{\text{micro}} = \frac{V_b P_a + V_a P_b}{V_b + V_a} = P_{\text{mid}} + \frac{\text{Spread}}{2} \cdot \text{OBI} $$

- If $V_b \gg V_a$ (heavy bids), the micro-price moves closer to the Ask, correctly anticipating an uptick.

---

## 5. Queue Position & Latency

For a market maker, your position in the FIFO queue at the best bid/ask is critical.

- **Queue Priority:** First In, First Out (FIFO).
- **Estimated Position:** If you join a queue of 1,000 shares, and 500 trade, you are now 500th in line.
- **Cancel-Replace Risk:** Modifying an order often sends you to the back of the queue.

### Probability of Fill
Depends on:
1.  **Queue Size ahead of you:** Smaller is better.
2.  **Trade Rate (Arrival Rate):** Higher volume increases fill probability.
3.  **Cancellation Rate:** Other traders cancelling moves you up the queue.

---

### Depth
```python
def market_depth(order_book, levels=5):
    """Total volume within N levels of best price."""
    bid_depth = sum(order_book['bids'][:levels]['size'])
    ask_depth = sum(order_book['asks'][:levels]['size'])
    return bid_depth, ask_depth
```

### Volume-Weighted Price
```python
def vwap_from_book(order_book, quantity):
    """Expected fill price for a market order of given size."""
    filled = 0
    cost = 0
    for price, size in order_book['asks']:
        fill = min(size, quantity - filled)
        cost += fill * price
        filled += fill
        if filled >= quantity:
            break
    return cost / filled if filled > 0 else None
```

## Order Book Events

| Event | Description | Signal |
|---|---|---|
| **New order** | Limit order placed | Intention to trade |
| **Cancel** | Order removed | Changed mind / spoofing |
| **Modify** | Size/price changed | Adjusting strategy |
| **Trade** | Orders matched | Information incorporated |
| **Sweep** | Large order clears multiple levels | Aggressive informed trader |

## Microstructure Signals

```python
def trade_flow_toxicity(trades, window=50):
    """
    VPIN (Volume-synchronized Probability of Informed Trading)
    High VPIN → more informed trading → wider spreads expected
    """
    buy_volume = trades[trades['side'] == 'buy']['volume'].rolling(window).sum()
    sell_volume = trades[trades['side'] == 'sell']['volume'].rolling(window).sum()
    total_volume = buy_volume + sell_volume

    vpin = abs(buy_volume - sell_volume) / total_volume
    return vpin
```

---

**Related:** [[Market Microstructure MOC]] | [[Bid-Ask Spread]] | [[Liquidity]] | [[Market Impact]] | [[Market Making Strategies]]
