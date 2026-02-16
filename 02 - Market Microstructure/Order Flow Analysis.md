# Order Flow Analysis

Order flow analysis studies the information content of trades and orders to predict short-term price movements. It bridges [[Market Microstructure MOC|market microstructure]] theory and practical [[Strategies MOC|trading strategies]], and is used extensively in [[High-Frequency Trading|HFT]] and institutional execution.

---

## Core Concepts

### Trade Classification
Every trade has a buyer and seller. **Who initiated?** The initiator hits the passive order.

**Lee-Ready Algorithm (1991):**
- If trade price > midpoint → **buyer-initiated** (buy aggressor)
- If trade price < midpoint → **seller-initiated** (sell aggressor)
- If at midpoint → use **tick test** (up-tick = buy, down-tick = sell)

```python
def classify_trades(prices, midpoints):
    """
    Lee-Ready trade classification.

    Returns: +1 (buyer-initiated), -1 (seller-initiated)
    """
    import numpy as np

    sign = np.where(prices > midpoints, 1,
                    np.where(prices < midpoints, -1, 0))

    # Tick test for ambiguous trades
    price_diff = np.diff(prices, prepend=prices[0])
    tick_sign = np.sign(price_diff)
    tick_sign[tick_sign == 0] = 1  # Default to buy

    # Use tick test where Lee-Ready is ambiguous
    sign[sign == 0] = tick_sign[sign == 0]

    return sign
```

---

## Order Flow Imbalance (OFI)

Net buying vs selling pressure at each price level:

$$OFI_t = \sum_{i} (\text{buy volume}_i - \text{sell volume}_i) \times \Delta P_i$$

### Simple Implementation
```python
def order_flow_imbalance(trades_df, window=100):
    """
    Compute rolling order flow imbalance.

    Parameters:
        trades_df: DataFrame with columns ['price', 'volume', 'side']
                   side: +1 (buy) or -1 (sell)

    Returns:
        Rolling OFI
    """
    signed_volume = trades_df['volume'] * trades_df['side']
    ofi = signed_volume.rolling(window).sum()
    return ofi
```

### OFI as a Predictor
Strong OFI predicts short-term returns (seconds to minutes):
$$r_{t+1} = \alpha + \beta \cdot OFI_t + \epsilon_t$$

Typical $R^2$: 5-15% at 1-second horizon (significant for HFT).

---

## VPIN — Volume-Synchronized Probability of Informed Trading

VPIN (Easley, Lopez de Prado, O'Hara, 2012) estimates the probability that a trade is information-driven, using volume-bucketed data rather than time-bucketed.

### Construction

1. **Volume buckets:** Group trades into buckets of fixed volume $V$
2. **Classify trades** into buy/sell (bulk classification)
3. **Compute VPIN:**

$$VPIN = \frac{\sum_{i=1}^{n} |V_i^B - V_i^S|}{n \cdot V}$$

Where:
- $V_i^B$ = buy volume in bucket $i$
- $V_i^S$ = sell volume in bucket $i$
- $n$ = number of buckets in the window

```python
import numpy as np
import pandas as pd

def compute_vpin(trades_df, bucket_volume, n_buckets=50):
    """
    Compute VPIN (Volume-Synchronized Probability of Informed Trading).

    Parameters:
        trades_df: DataFrame with ['volume', 'side'] columns
                   side: +1 (buy) or -1 (sell)
        bucket_volume: Volume per bucket
        n_buckets: Number of buckets for rolling VPIN

    Returns:
        VPIN time series
    """
    # Assign trades to volume buckets
    trades_df = trades_df.copy()
    trades_df['cum_volume'] = trades_df['volume'].cumsum()
    trades_df['bucket'] = (trades_df['cum_volume'] / bucket_volume).astype(int)

    # Aggregate buy/sell volume per bucket
    buy_vol = trades_df[trades_df['side'] == 1].groupby('bucket')['volume'].sum()
    sell_vol = trades_df[trades_df['side'] == -1].groupby('bucket')['volume'].sum()

    bucket_df = pd.DataFrame({'buy': buy_vol, 'sell': sell_vol}).fillna(0)
    bucket_df['imbalance'] = abs(bucket_df['buy'] - bucket_df['sell'])

    # Rolling VPIN
    vpin = bucket_df['imbalance'].rolling(n_buckets).sum() / \
           (n_buckets * bucket_volume)

    return vpin


def bulk_classify(prices, volumes, bucket_volume):
    """
    Bulk Volume Classification (BVC) — no trade-by-trade classification needed.
    Classifies volume based on price movement within each bucket.
    """
    # Bucket price returns
    cum_vol = volumes.cumsum()
    bucket_ids = (cum_vol / bucket_volume).astype(int)

    bucket_close = prices.groupby(bucket_ids).last()
    bucket_open = prices.groupby(bucket_ids).first()
    bucket_vol = volumes.groupby(bucket_ids).sum()

    # Standardize returns
    returns = (bucket_close - bucket_open) / bucket_open
    from scipy.stats import norm
    z = returns / returns.std()

    # Buy fraction = CDF of normalized return
    buy_pct = norm.cdf(z)
    buy_vol = bucket_vol * buy_pct
    sell_vol = bucket_vol * (1 - buy_pct)

    return buy_vol, sell_vol
```

### VPIN Interpretation

| VPIN Level | Interpretation | Action |
|-----------|----------------|--------|
| < 0.2 | Low toxicity, normal flow | Normal trading |
| 0.2 - 0.4 | Moderate toxicity | Widen spreads, reduce size |
| 0.4 - 0.6 | High toxicity (informed trading) | Significant caution |
| > 0.6 | Extreme toxicity | Withdraw from market |

**Flash Crash link:** VPIN spiked before the May 6, 2010 Flash Crash — it can serve as an early warning indicator.

---

## Kyle's Lambda — Price Impact of Order Flow

Kyle (1985) showed that price changes are proportional to order flow:

$$\Delta P = \lambda \cdot OFI + \epsilon$$

Where $\lambda$ measures the **information content per unit of order flow** (also called Kyle's lambda or price impact coefficient).

```python
def kyles_lambda(price_changes, ofi, window=1000):
    """
    Estimate Kyle's lambda (price impact per unit order flow).

    High lambda = illiquid market (informed traders present)
    Low lambda = liquid market (uninformed flow dominates)
    """
    from sklearn.linear_model import LinearRegression

    results = []
    for i in range(window, len(price_changes)):
        dp = price_changes.iloc[i-window:i].values.reshape(-1, 1)
        of = ofi.iloc[i-window:i].values.reshape(-1, 1)
        mask = ~(np.isnan(dp.flatten()) | np.isnan(of.flatten()))
        if mask.sum() > 50:
            reg = LinearRegression().fit(of[mask], dp[mask])
            results.append(reg.coef_[0][0])
        else:
            results.append(np.nan)

    return pd.Series(results, index=price_changes.index[window:])
```

---

## Order Flow Toxicity and Market Making

For [[Market Making Strategies|market makers]], order flow toxicity determines profitability:

- **Low toxicity:** Most flow is uninformed → market maker earns spread
- **High toxicity:** Informed traders present → market maker gets adversely selected

### Adverse Selection Framework
$$E[\text{MM profit per trade}] = \text{spread}/2 - \lambda \cdot P(\text{informed})$$

When $\lambda \cdot P(\text{informed}) > \text{spread}/2$, the market maker loses money.

---

## Applications

### 1. Execution Quality
Monitor OFI during execution to detect adverse flow:
- If filling into toxic flow → **slow down execution**
- If filling into uninformed flow → **accelerate**
- See [[Smart Order Routing]] and [[Implementation Shortfall]]

### 2. Short-Term Alpha
OFI at various horizons predicts returns:
- 1-second OFI → HFT signal
- 1-minute OFI → Intraday momentum
- Daily OFI → Swing trade signal

### 3. Risk Management
VPIN spikes as early warning for tail events:
- Integrate into [[Risk Management MOC|risk system]] as a regime indicator
- Reduce exposure when VPIN > threshold

### 4. Fair Value Estimation
Order book imbalance predicts the next mid-price:
$$\text{Fair Value} = \text{Mid} + \alpha \cdot \frac{Q_{\text{bid}} - Q_{\text{ask}}}{Q_{\text{bid}} + Q_{\text{ask}}}$$
See [[Order Book Dynamics]] and [[Price Discovery]].

---

## Related Notes
- [[Order Book Dynamics]] — Limit order book structure
- [[Market Microstructure MOC]] — Parent section
- [[Market Impact]] — How trades move prices
- [[Bid-Ask Spread]] — Spread as adverse selection compensation
- [[Price Discovery]] — How information enters prices
- [[High-Frequency Trading]] — Primary user of order flow signals
- [[Market Making Strategies]] — Toxicity-aware market making
- [[Liquidity]] — Relationship between flow and liquidity
- [[Tick Data and Trade Data]] — Raw data for order flow analysis
