# Market Making Strategies

**Core Idea:** Continuously quote bid and ask prices, profiting from the [[Bid-Ask Spread]]. You are the "house" — providing [[Liquidity]] and getting paid for it.

---

## How Market Making Works

```
You quote:  BID $99.98  ×  ASK $100.02
Someone buys from you at $100.02 (you sell)
Someone sells to you at $99.98 (you buy)
Your profit: $0.04 per share (spread capture)
```

**Revenue model:** Spread × Volume - Adverse Selection Losses - Inventory Risk

## The Market Maker's Dilemma

You face two types of counterparties:
1. **Uninformed traders** — Want to trade for non-information reasons → PROFIT
2. **Informed traders** — Know something you don't → LOSS (adverse selection)

The spread must compensate for adverse selection:
```
Optimal Spread = Adverse Selection Cost + Inventory Cost + Order Processing Cost
```

See [[Market Microstructure MOC]] for the theory.

## Avellaneda-Stoikov Model

The foundational model for optimal market making:

```
Reservation Price:
  r = s - q·γ·σ²·(T-t)

Optimal Spread:
  δ = γ·σ²·(T-t) + (2/γ)·ln(1 + γ/k)

Where:
  s = mid price
  q = current inventory
  γ = risk aversion parameter
  σ = volatility
  T-t = time remaining
  k = order arrival intensity parameter
```

**Intuition:**
- Higher volatility → wider spreads (more risk)
- Positive inventory → lower ask (want to sell), higher bid (don't want to buy more)
- Near end of day → tighter spreads (reduce inventory pressure)

## Implementation

```python
import numpy as np

class MarketMaker:
    def __init__(self, gamma=0.1, sigma=0.02, k=1.5, tick_size=0.01):
        self.gamma = gamma    # Risk aversion
        self.sigma = sigma    # Volatility
        self.k = k            # Order arrival intensity
        self.tick_size = tick_size
        self.inventory = 0
        self.max_inventory = 100

    def compute_quotes(self, mid_price, time_remaining=1.0):
        """
        Compute optimal bid and ask prices.
        """
        # Reservation price (inventory-adjusted mid)
        reservation = mid_price - self.inventory * self.gamma * self.sigma**2 * time_remaining

        # Optimal spread
        spread = (self.gamma * self.sigma**2 * time_remaining +
                  (2/self.gamma) * np.log(1 + self.gamma/self.k))

        bid = reservation - spread/2
        ask = reservation + spread/2

        # Round to tick size
        bid = np.floor(bid / self.tick_size) * self.tick_size
        ask = np.ceil(ask / self.tick_size) * self.tick_size

        # Inventory limits
        if self.inventory >= self.max_inventory:
            bid = 0  # Don't buy more
        if self.inventory <= -self.max_inventory:
            ask = float('inf')  # Don't sell more

        return bid, ask

    def on_fill(self, side, price, quantity):
        """Update inventory on fill."""
        if side == 'BUY':
            self.inventory += quantity
        else:
            self.inventory -= quantity

    def pnl_from_spread(self, bid_fills, ask_fills):
        """Calculate P&L from spread capture."""
        revenue = sum(p * q for p, q in ask_fills) - sum(p * q for p, q in bid_fills)
        net_inventory = sum(q for _, q in bid_fills) - sum(q for _, q in ask_fills)
        return revenue, net_inventory
```

## Key Parameters

| Parameter | Effect When Increased |
|---|---|
| **Spread width** | More profit per trade, fewer fills |
| **Risk aversion (γ)** | Wider spreads, faster inventory reduction |
| **Quote size** | More fills, more inventory risk |
| **Max inventory** | More risk, more opportunity |
| **Refresh rate** | Faster adaptation, more cancellations |

## Risk Management for Market Makers

### Inventory Risk
Your biggest risk. Holding inventory exposes you to directional price moves.

**Controls:**
- Skew quotes to reduce inventory (Avellaneda-Stoikov)
- Hard inventory limits
- Hedge with index futures/ETFs
- End-of-day flatten rule

### Adverse Selection
Informed traders pick you off.

**Detection signals:**
- Large order hitting your quote
- Order flow imbalance
- Unusual volume patterns
- News events

**Protection:**
- Widen spreads when adverse selection detected
- Reduce quote size near news events
- Cancel quotes when [[Order Book Dynamics|order book]] pressure detected
- Minimum quote lifetime (avoid sniping)

## Requirements

| Requirement | Detail |
|---|---|
| **Speed** | Microsecond-level quote updates (see [[Low-Latency Systems]]) |
| **Capital** | Enough to hold inventory through adverse moves |
| **Data** | Real-time L2/L3 order book data |
| **Rebates** | Maker fee rebates are essential to profitability |
| **Co-location** | Often necessary (see [[Co-location and Proximity]]) |

## Profitability Drivers

```
P&L = (Spread Captured × Volume) - Adverse Selection - Inventory Losses - Costs

Typical decomposition:
  Gross spread revenue:     +$10,000/day
  Adverse selection:        -$4,000/day
  Inventory P&L:            -$1,000/day (volatile)
  Exchange fees/rebates:    +$500/day
  Infrastructure costs:     -$2,000/day
  ─────────────────────────────────────
  Net P&L:                  +$3,500/day
```

---

**Related:** [[Bid-Ask Spread]] | [[Order Book Dynamics]] | [[Market Microstructure MOC]] | [[High-Frequency Trading]] | [[Liquidity]] | [[Low-Latency Systems]]
