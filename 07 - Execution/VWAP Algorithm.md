# VWAP Algorithm (Volume-Weighted Average Price)

The **VWAP Algorithm** is the industry-standard execution strategy used by institutional traders to minimize market impact while matching the average price of the day. Unlike [[TWAP Algorithm]], which trades linearly over time, VWAP trades in proportion to the historical or expected intraday volume profile.

---

## 1. The VWAP Benchmark

VWAP is calculated as the sum of the dollars traded divided by the total shares traded:

$$P_{VWAP} = \frac{\sum (Price_i \times Volume_i)}{\sum Volume_i}$$

A "successful" execution is one where the average fill price is better than (lower for buys, higher for sells) the market VWAP for that period.

---

## 2. The Intraday Volume Profile (U-Shape)

Market volume is not distributed evenly. It typically follows a "U-Shape":
- **High Volume:** Market Open (9:30 AM) and Market Close (4:00 PM).
- **Low Volume:** Midday (Lunchtime lull).

The VWAP algorithm estimates this profile (e.g., in 5-minute bins) using historical data and adjust the trading rate accordingly.

---

## 3. Static vs. Dynamic VWAP

### A. Static VWAP
Uses a pre-calculated historical volume profile.
- **Pros:** Simple, predictable.
- **Cons:** Fails if the current day's volume deviates significantly from history (e.g., during a news event).

### B. Dynamic VWAP (Adaptive)
Adjusts the trading schedule in real-time based on the volume already observed today.
- **Pros:** Better at matching the *actual* market VWAP of the day.
- **Cons:** Can lead to "chasing" volume if a massive spike occurs late in the day.

---

## 4. Python: Estimating Volume Profile

```python
import pandas as pd
import numpy as np

def calculate_historical_volume_profile(df_list):
    """
    Calculates the average percentage of daily volume in each 5-minute bin.
    """
    profiles = []
    for df in df_list:
        # Group by time of day
        daily_vol = df['volume'].sum()
        profile = df.groupby(df.index.time)['volume'].sum() / daily_vol
        profiles.append(profile)
    
    # Average across all days
    avg_profile = pd.concat(profiles, axis=1).mean(axis=1)
    return avg_profile

# Usage in algorithm:
# If bin 9:30-9:35 typically has 5% of volume, 
# VWAP will aim to trade 5% of your total order in that window.
```

---

## 5. When to Use VWAP

- **High Liquidity Assets:** Works best in large-cap stocks with predictable volume.
- **Passive Execution:** When there is no extreme urgency to fill.
- **Benchmark Matching:** For mutual funds or pension funds whose mandate is to match the day's average price.

---

## 6. VWAP Gaming & Pitfalls

- **Information Leakage:** If your participation rate is too high (e.g., > 20% of market volume), other traders will spot your VWAP and trade ahead of you.
- **Market Impact:** Although VWAP minimizes impact, trading 1 million shares will still move the price regardless of the schedule.
- **The "Tail" Risk:** If you have 20% of your order left to trade in the last 30 minutes, you are forced to be aggressive, which often leads to poor fills.

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[TWAP Algorithm]] — Time-weighted alternative
- [[Implementation Shortfall]] — A more rigorous benchmark
- [[Market Impact Models]] — Modeling the cost of VWAP
- [[Trading Sessions and Hours]] — Context for the U-shape
