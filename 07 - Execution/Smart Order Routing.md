# Smart Order Routing (SOR)

**Smart Order Routing (SOR)** is an automated process used by algorithmic trading engines to manage order execution across multiple, fragmented liquidity venues. The goal is to achieve the best possible execution price (NBBO) while minimizing market impact and transaction costs.

---

## 1. The Challenge: Market Fragmentation

In modern markets (especially US Equities and Crypto), a single asset is traded on dozens of venues:
- **Lit Exchanges:** NYSE, NASDAQ, Cboe (Public order books).
- **Dark Pools:** Goldman Sachs Sigma X, JPM Cross, Barclays LX (Hidden liquidity).
- **Internalizers / Market Makers:** Citadel, Virtu (Buying retail flow).

An SOR's job is to "see" through this fragmentation and find the optimal path for an order.

---

## 2. Routing Logic & Strategies

### A. Spray (Sequential or Parallel)
Sending small slices of a large order to every venue that shows size at the target price.
- **Parallel Spray:** Sending orders to all venues simultaneously to minimize latency risk.
- **Sequential Spray:** Hitting the best venue first, then the next, to avoid over-filling.

### B. Passive vs. Aggressive Routing
- **Aggressive:** Hitting the bid/ask to get immediate fills (paying the spread).
- **Passive:** Placing limit orders across multiple books to capture the rebate (see [[Maker-Taker Fee Model]]).

### C. Dark Pool Sniping
Prioritizing hidden liquidity venues first. If no fill is found in the "dark," the SOR routes to the "lit" market. This minimizes information leakage.

---

## 3. Key SOR Decision Factors

| Factor | Description |
|--------|-------------|
| **NBBO** | National Best Bid and Offer. Routing to the venue with the best price is a legal requirement (Reg NMS). |
| **Liquidity Depth** | Routing to venues with the largest queues to ensure full fills. |
| **Venue Fees/Rebates** | Some venues pay you to provide liquidity. An SOR calculates the "Net Price" (Price + Fee/Rebate). |
| **Fill Probability** | Historical data on which venues provide the fastest and most reliable fills. |
| **Latency** | Physical distance to the venue (see [[Co-location and Proximity]]). |

---

## 4. Python Simulation: Basic SOR Router

```python
import numpy as np

class SmartOrderRouter:
    def __init__(self, venues):
        """
        venues: list of dicts {'name': str, 'price': float, 'size': int, 'fee': float}
        """
        self.venues = venues

    def route_order(self, total_qty, side='buy'):
        """
        Routes a buy order to the cheapest venues (including fees).
        """
        # Calculate Net Price
        for v in self.venues:
            v['net_price'] = v['price'] + v['fee'] if side == 'buy' else v['price'] - v['fee']
        
        # Sort venues by Net Price
        sorted_venues = sorted(self.venues, key=lambda x: x['net_price'], reverse=(side == 'sell'))
        
        fills = []
        remaining_qty = total_qty
        
        for v in sorted_venues:
            if remaining_qty <= 0: break
            
            fill_qty = min(remaining_qty, v['size'])
            fills.append({'venue': v['name'], 'qty': fill_qty, 'price': v['price']})
            remaining_qty -= fill_qty
            
        return fills, remaining_qty

# Example Usage
venues = [
    {'name': 'NASDAQ', 'price': 150.01, 'size': 1000, 'fee': 0.003},
    {'name': 'NYSE', 'price': 150.00, 'size': 500, 'fee': 0.001},
    {'name': 'DARK_POOL', 'price': 150.00, 'size': 2000, 'fee': 0.0}
]

sor = SmartOrderRouter(venues)
fills, unplaced = sor.route_order(2000)
print(f"Fills: {fills}")
```

---

## 5. Adverse Selection & Signaling Risk

A poorly designed SOR can "telegraph" its intentions. If an SOR hits multiple lit exchanges in a predictable sequence, HFT algos will detect the pattern and front-run the remaining size on other venues.

---

## Related Notes
- [[Execution MOC]] — Broader execution context
- [[Order Routing]] — Physical path of the order
- [[Execution Venues]] — Types of marketplaces
- [[Reg NMS]] — US regulatory framework for SOR
- [[Maker-Taker Fee Model]] — Understanding the economics of routing
- [[Market Impact Models]] — Why we split orders
