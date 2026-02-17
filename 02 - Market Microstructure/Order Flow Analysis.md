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

## The Information Hierarchy of Trades

Not all order flow is created equal. The "information content" of a trade depends heavily on how it is executed. Understanding this hierarchy is crucial for interpreting order flow data correctly.

| Trade Type | Information Content | Typical Player | Market Impact |
| :--- | :--- | :--- | :--- |
| **Aggressive Market Orders** | **Very High** | Informed trader needing immediate execution (e.g., alpha signal, stop-loss trigger). | High, both temporary and permanent. This is the "price of immediacy." |
| **Aggressive Limit Orders** | **High** | Urgently repositioning trader, willing to cross the spread but wanting price control. | Moderate to High. Signals strong directional intent. |
| **Midpoint Peg / Passive Fills** | **Low to Medium** | Patient institutional execution (e.g., [[VWAP Algorithm|VWAP algo]]), retail investors. | Low. These trades are designed to minimize impact by capturing spread. |
| **"Hidden" Orders (Icebergs)** | **Very High (if detected)** | Large institution trying to execute a big block without revealing its full size. | Low initial impact, but can cause a "spring-loading" effect if the hidden volume is depleted. |
| **Market Maker Flow** | **Low (generally)** | Internalizing flow, hedging, earning spread. Typically uninformed. | Low, often offsetting. Their goal is to *not* have a directional view. |

**Key takeaway:** A 10,000-share market order that sweeps three levels of the book contains far more information and will have a greater impact than 100 separate 100-share limit orders resting passively on the bid. Simple OFI, which just sums up volume, misses this crucial context. Advanced order flow models aim to weight trades by their likely information content.

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

---

## VPIN — Volume-Synchronized Probability of Informed Trading

VPIN, developed by Easley, Lopez de Prado, and O'Hara (2012), is a widely-cited indicator designed to estimate the probability of informed trading in near real-time. It is a practical and computationally efficient evolution of the earlier, more theoretical PIN (Probability of Informed Trading) model.

### Theoretical Background: From PIN to VPIN

The original **PIN model** assumes that trades come from two sources: uninformed liquidity traders (arriving at a rate $\epsilon$) and informed traders who receive new information (arriving at a rate $\mu$). Good news arrives with probability $\alpha$, bad news with probability $(1-\alpha)$. The model uses maximum likelihood estimation on trade data to solve for these latent parameters. **PIN = $\frac{\alpha \mu}{\alpha \mu + \epsilon}$**.

**PIN's drawbacks:**
-   Requires complex, slow maximum-likelihood estimation.
-   Unstable and not suitable for high-frequency, real-time use.

**VPIN's innovation:**
VPIN's key insight is to bypass the complex estimation by assuming that order imbalance in **volume-time** is a good proxy for the latent order flow imbalance in the PIN model. Instead of estimating the arrival rates of informed vs. uninformed traders, it directly measures the imbalance of buy vs. sell volume.

### Volume-Synchronized Bucketing

The second key innovation is the use of **volume-time** instead of clock-time. The market's "clock" doesn't tick in seconds, it ticks in trades and volume.
1.  **Define a Volume Bucket:** A fixed amount of trading volume is chosen as the "unit of time" (e.g., 1/50th of the average daily volume).
2.  **Group Trades:** Concatentate trades sequentially until the cumulative volume fills a bucket.
3.  **Analyze Buckets:** Each bucket represents an equal amount of market activity, making them more comparable than, for example, a 5-minute time bar, which could contain vastly different levels of activity.

This synchronization makes the resulting imbalance measure more robust to fluctuations in trading activity throughout the day.

### VPIN Formula and Construction

The VPIN for a rolling window of $n$ volume buckets is the sum of the absolute imbalance in each bucket, divided by the total volume in the window.

$$VPIN = \frac{\sum_{i=1}^{n} |V_i^B - V_i^S|}{n \cdot V}$$

Where:
-   $V_i^B$ = buy volume in bucket $i$
-   $V_i^S$ = sell volume in bucket $i$
-   $V$ is the volume of a single bucket.
-   $n$ is the number of buckets in the rolling window.

```python
import numpy as np
import pandas as pd

def compute_vpin(trades_df, bucket_volume, n_buckets=50):
    """
    Compute VPIN (Volume-Synchronized Probability of Informed Trading).

    Parameters:
        trades_df: DataFrame with ['volume', 'side'] columns
                   side: +1 (buy) or -1 (sell)
        bucket_volume: Volume per bucket (e.g., 1/50th of ADV)
        n_buckets: Number of buckets for the rolling VPIN window

    Returns:
        VPIN time series, indexed by bucket number.
    """
    trades_df = trades_df.copy()
    trades_df['cum_volume'] = trades_df['volume'].cumsum()
    trades_df['bucket'] = (trades_df['cum_volume'] / bucket_volume).astype(int)

    # Aggregate buy/sell volume per bucket
    buy_vol = trades_df[trades_df['side'] == 1].groupby('bucket')['volume'].sum()
    sell_vol = trades_df[trades_df['side'] == -1].groupby('bucket')['volume'].sum()

    bucket_df = pd.DataFrame({'buy': buy_vol, 'sell': sell_vol}).fillna(0)
    bucket_df['imbalance'] = abs(bucket_df['buy'] - bucket_df['sell'])

    # Rolling VPIN calculation
    vpin = bucket_df['imbalance'].rolling(n_buckets).sum() / (n_buckets * bucket_volume)

    return vpin
```

### VPIN Interpretation and Limitations

| VPIN Level | Interpretation | Action for Liquidity Provider |
| :--- | :--- | :--- |
| < 0.2 | Low toxicity, normal flow. | Normal operations, capture spread. |
| 0.2 - 0.4 | Moderate toxicity. | Widen spreads, potentially reduce size. |
| > 0.4 | High toxicity, informed trading is dominant. | Drastically widen spreads, reduce size, or hedge. |
| > 0.6-0.8 | Extreme toxicity, "liquidity crisis". | Withdraw from the market to avoid severe losses. |

**VPIN as a Flash Crash Predictor:** VPIN famously spiked to extreme levels in the hour preceding the May 6, 2010 Flash Crash, suggesting it can act as an early-warning system for market fragility and impending liquidity crises.

**Critiques and Limitations:**
-   **Parameter Sensitivity:** The choice of bucket volume ($V$) and the number of rolling buckets ($n$) can significantly alter the VPIN series. There is no universally optimal setting.
-   **Trade Classification:** VPIN's accuracy depends on the underlying trade classification algorithm (e.g., Lee-Ready). In markets with high volumes of dark pool or midpoint trades, this can be noisy.
-   **Causality vs. Correlation:** Does high VPIN *cause* crashes, or does it simply correlate with the high volume and volatility that precede crashes? The academic debate is ongoing. Some argue it is more of a volatility proxy than a pure measure of toxicity.
-   **Not a Standalone Signal:** VPIN is a risk management and regime-filtering tool, not a simple "buy/sell" alpha signal. Using it requires context.

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

## Putting It All Together: A Workflow Example

This example demonstrates the end-to-end process of taking raw trade data and computing the core order flow metrics.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate_trade_data(n_trades=50000):
    """Simulates a DataFrame of raw trade and quote data."""
    base_price = 100
    price_drift = 0.00001
    volatility = 0.0001
    
    # Simulate a random walk for mid-price
    price_moves = np.random.normal(loc=price_drift, scale=volatility, size=n_trades)
    mid_price = base_price + np.cumsum(price_moves)
    
    # Simulate spread and trade prices
    spread = np.random.uniform(0.01, 0.03, size=n_trades)
    trade_prices = mid_price + spread/2 * np.random.choice([-1, 1], size=n_trades)
    
    # Simulate volume
    volumes = np.random.randint(100, 1000, size=n_trades)
    
    timestamps = pd.to_datetime(pd.to_datetime('2023-01-01 09:30:00') + 
                                pd.to_timedelta(np.arange(n_trades) * 100, unit='ms'))
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'price': trade_prices,
        'volume': volumes,
        'midpoint': mid_price
    }).set_index('timestamp')
    
    return df

def full_order_flow_analysis(trades_df):
    """
    Runs a full workflow of order flow analysis on a trade DataFrame.
    """
    # 1. Classify Trades using Lee-Ready
    trades_df['side'] = classify_trades(trades_df['price'], trades_df['midpoint'])
    
    # 2. Compute Order Flow Imbalance (OFI)
    # Using a 50-trade window
    trades_df['ofi'] = order_flow_imbalance(trades_df, window=50)
    
    # 3. Compute VPIN
    # Set bucket volume to 1/50th of total daily volume
    total_volume = trades_df['volume'].sum()
    bucket_volume = total_volume / 50
    vpin_series = compute_vpin(trades_df, bucket_volume, n_buckets=50)
    
    # 4. Compute Kyle's Lambda
    # Using 1-second price changes
    price_changes = trades_df['midpoint'].diff()
    trades_df['kyles_lambda'] = kyles_lambda(price_changes, trades_df['ofi'], window=1000)
    
    # --- Visualization ---
    fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    
    # Plot 1: Price and OFI
    ax1 = axes[0]
    ax1.plot(trades_df.index, trades_df['midpoint'], label='Midpoint Price', color='navy')
    ax1.set_ylabel('Price ($)')
    ax1.set_title('Midpoint Price and Order Flow Imbalance (OFI)', fontsize=14)
    ax1.legend(loc='upper left')
    ax1b = ax1.twinx()
    ax1b.fill_between(trades_df.index, 0, trades_df['ofi'],
                      where=trades_df['ofi'] >= 0, facecolor='green', alpha=0.5, label='Buy OFI')
    ax1b.fill_between(trades_df.index, 0, trades_df['ofi'],
                      where=trades_df['ofi'] < 0, facecolor='red', alpha=0.5, label='Sell OFI')
    ax1b.set_ylabel('Order Flow Imbalance')
    ax1b.legend(loc='upper right')
    
    # Plot 2: VPIN
    ax2 = axes[1]
    # Align VPIN series with main dataframe for plotting
    vpin_aligned = vpin_series.reindex(trades_df.bucket, method='ffill')
    vpin_aligned.index = trades_df.index
    ax2.plot(vpin_aligned.index, vpin_aligned, label='VPIN (50 buckets)', color='purple')
    ax2.axhline(0.4, color='orange', linestyle='--', label='High Toxicity Threshold (0.4)')
    ax2.axhline(0.6, color='red', linestyle='--', label='Extreme Toxicity Threshold (0.6)')
    ax2.set_ylabel('VPIN')
    ax2.set_title('Volume-Synchronized Probability of Informed Trading (VPIN)', fontsize=14)
    ax2.legend()
    
    # Plot 3: Kyle's Lambda
    ax3 = axes[2]
    trades_df['kyles_lambda'].plot(ax=ax3, label="Kyle's Lambda (Rolling 1000 trades)", color='darkred')
    ax3.set_ylabel('Lambda (Price Impact)')
    ax3.set_title("Kyle's Lambda: Market Impact per Unit of Order Flow", fontsize=14)
    ax3.legend()
    
    plt.tight_layout()
    plt.show()
    
    return trades_df

# --- Main execution ---
# This part is for standalone execution and would be run in a notebook
# if __name__ == '__main__':
#     # 1. Simulate data
#     raw_trades = simulate_trade_data(n_trades=50000)
    
#     # 2. Run analysis by calling the functions defined in this note
#     # Note: The functions classify_trades, order_flow_imbalance, etc. must be defined
#     # analysis_results = full_order_flow_analysis(raw_trades)
    
#     # print("Analysis Complete. Displaying final DataFrame sample:")
#     # print(analysis_results.tail())

```

---

## Order Flow Toxicity and Adverse Selection

Order flow is "toxic" to a liquidity provider (like a market maker) if it leads to consistent losses through **adverse selection**. Adverse selection occurs when the market maker provides a quote to a trader who has superior information about the future price of the asset.

-   **Informed Trader Buys:** The informed trader buys from the market maker because they know the price is about to go up. The market maker is now short an asset that is appreciating in value.
-   **Informed Trader Sells:** The informed trader sells to the market maker because they know the price is about to go down. The market maker is now long an asset that is depreciating in value.

The profit of a market maker can be modeled as:
$$ E[\text{Profit}] = (\text{Spread Earned}) - (\text{Losses to Adverse Selection}) $$

### Measuring Toxicity

Toxicity is not directly observable but can be estimated. VPIN is one such estimate. Another is the probability of informed trading (PIN), from which VPIN is derived. A simpler, practical measure is the **realized spread**, which captures the profitability of a market-making strategy.

**Realized Spread Calculation:**
For a buy order filled by a market maker at the ask price at time `t`:
$$ \text{Realized Spread}_t = (\text{Ask}_t - \text{Midpoint}_{t+ \Delta t}) $$
A negative average realized spread indicates that, on average, the price moved against the market maker after the trade, implying the flow was toxic.

### The Smile of Toxicity
Toxicity is not constant; it varies with trade size and speed.
- **Small, slow trades:** Likely uninformed (retail flow, portfolio rebalancing). Low toxicity.
- **Large, aggressive trades:** More likely to be informed (hedge fund executing on an alpha signal). High toxicity.

This relationship is sometimes called the "toxicity smile" and is why market makers quote wider spreads for larger order sizes. They are charging a premium for the increased risk of being adversely selected.

### The Market Maker's Response
A market maker's survival depends on managing toxicity. Their response is governed by their inventory and their perception of flow toxicity:
- **Low Toxicity:** Tighten spreads to capture more uninformed flow and earn the bid-ask spread.
- **High Toxicity (High VPIN):**
    1.  **Widen Spreads:** Increase the cost for traders, creating a buffer against adverse selection.
    2.  **Reduce Quoted Size:** Offer less liquidity to minimize potential losses.
    3.  **Skew Quotes:** If holding a long inventory and toxicity spikes, lower both bid and ask prices to encourage selling and discourage further buying.
    4.  **Withdraw:** In extreme cases (like a VPIN > 0.6), pull all quotes and wait for toxicity to subside. This is a key mechanism that can lead to flash crashes, as liquidity evaporates market-wide.

Understanding order flow toxicity is therefore central to any strategy that involves providing liquidity, not just dedicated market making.

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
