# Commodities Trading Strategies

Commodities (Energy, Metals, Agriculture) are distinct from financial assets because they are physical goods with storage costs, production cycles, and weather dependencies. Most trading happens via **Futures Contracts**.

---

## 1. The Forward Curve: Contango vs. Backwardation

Understanding the shape of the futures curve is critical.

### Contango (Normal Market)
- **Futures Price > Spot Price** ($F_t > S_t$).
- Typical for markets with ample supply and storage costs (e.g., Oil, Wheat).
- **Roll Yield:** Negative. Long positions lose money as the contract approaches expiry and converges to spot.

### Backwardation (Inverted Market)
- **Spot Price > Futures Price** ($S_t > F_t$).
- Occurs during shortages or high immediate demand (convenience yield > storage cost).
- **Roll Yield:** Positive. Long positions make money as futures converge *up* to spot.

---

## 2. Roll Yield Strategy

The primary source of return for passive commodity investors is the **Roll Yield**.

$$R_{Roll} \approx \frac{F_{near} - F_{far}}{P_{spot}}$$

- **Strategy:** Buy commodities in backwardation (positive roll) and short those in contango (negative roll).
- **Implementation:** Long-short portfolio based on the slope of the term structure.

---

## 3. Seasonality

Commodities exhibit strong seasonal patterns due to weather and demand cycles.

- **Natural Gas:** Winter heating demand peaks in Jan/Feb.
- **Agriculture (Corn/Soybeans):** Planting (Spring) vs. Harvest (Fall). Prices tend to bottom at harvest due to supply glut.
- **Gasoline:** Summer driving season in the US.

---

## 4. Spread Trading (Calendar Spreads)

Instead of outright directional bets, traders trade the difference between two contract months.

- **Bull Spread:** Long Near Month / Short Far Month. Profits if the market tightens (backwardation increases).
- **Bear Spread:** Short Near Month / Long Far Month. Profits if the market loosens (contango increases).
- **Crack Spread:** Long Crude Oil / Short Gasoline + Heating Oil. Refiner margin.

---

## 5. Momentum (Trend Following)

Commodities trend well due to slow supply/demand adjustments (e.g., building a mine takes years).
- **Time Series Momentum:** Long if price > 12-month MA.
- **Cross-Sectional Momentum:** Long strongest commodities, short weakest.

---

## Python Implementation: Calculate Roll Yield

```python
import pandas as pd

def calculate_roll_yield(near_price, far_price, months_diff):
    """
    Calculate annualized roll yield from futures curve.
    
    Parameters:
        near_price: Price of near-term contract
        far_price: Price of longer-dated contract
        months_diff: Number of months between contracts
    """
    # Log roll yield approximation
    raw_yield = (near_price - far_price) / near_price
    annualized_yield = raw_yield * (12 / months_diff)
    
    state = "Backwardation" if near_price > far_price else "Contango"
    
    return annualized_yield, state

# Example: Crude Oil (CL)
# Spot/Near: $80, 6-Month Future: $75
roll, state = calculate_roll_yield(80, 75, 6)
print(f"Market State: {state}")
print(f"Annualized Roll Yield: {roll:.2%}")
# Result: Backwardation, +12.5% yield (Long makes money)
```

---

## Related Notes
- [[Strategies MOC]] — Master navigation
- [[Trend Following]] — Key strategy in commodities
- [[Macro Economics]] — Demand drivers (China, Inflation)
- [[Fixed Income]] — Inflation hedging with commodities
- [[Derivatives Pricing]] — Futures pricing (Cost of Carry model)
