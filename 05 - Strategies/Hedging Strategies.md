# Hedging Strategies

Hedging is the practice of reducing or eliminating unwanted risks in a portfolio. In quantitative finance, hedging is rarely about eliminating *all* risk, but rather isolating the specific risk factor (alpha) you want to bet on.

---

## 1. Delta Hedging (Directional Neutrality)

The most fundamental form of hedging for options traders.

### Concept
- **Objective:** Neutralize exposure to small price movements in the underlying asset ($S$).
- **Method:** For every option contract held, trade $-\Delta$ shares of the underlying.
- **Dynamic:** Delta changes as $S$ moves (Gamma) and time passes (Charm), requiring continuous rebalancing.

### P&L Attribution
$$P\&L \approx \frac{1}{2}\Gamma (\Delta S)^2 + \Theta \Delta t$$
- If realized volatility $>$ implied volatility, you make money (Gamma profit > Theta bleed).

---

## 2. Gamma Scalping

A strategy for long volatility traders.

1.  **Start:** Buy a straddle (Long Call + Long Put) and hedge to be Delta Neutral.
2.  **Price Rises:** Delta becomes positive. **Sell** stock to re-hedge.
3.  **Price Falls:** Delta becomes negative. **Buy** stock to re-hedge.
4.  **Result:** You are constantly "buying low and selling high" around the strike price. This scalping profit offsets the Theta decay.

---

## 3. Minimum Variance Hedging (Futures)

Hedging a spot position with a correlated futures contract (e.g., hedging a tech portfolio with NASDAQ futures).

### Optimal Hedge Ratio ($h^*$)
Minimize the variance of the hedged portfolio $P_H = S - hF$.

$$h^* = ho \frac{\sigma_S}{\sigma_F}$$

Which is simply the slope ($\beta$) from a linear regression of spot returns on futures returns.
$$R_S = \alpha + \beta R_F + \epsilon$$

---

## 4. Tail Risk Hedging

Protecting against "Black Swan" events (3-sigma moves).

- **OTM Puts:** Buying deep OTM puts. Costly (bleed) during normal markets but pays off convexly in a crash.
- **VIX Calls:** Long volatility exposure. VIX tends to spike when equities crash (negative correlation).
- **Trend Following:** Managed futures strategies often perform well during prolonged crises (e.g., 2008, 2022).

---

## Python Implementation: Minimum Variance Hedge Ratio

```python
import numpy as np
from sklearn.linear_model import LinearRegression

def optimal_hedge_ratio(spot_returns, futures_returns):
    """
    Calculate the optimal hedge ratio (beta) to minimize variance.
    """
    model = LinearRegression()
    # Reshape for sklearn
    X = futures_returns.values.reshape(-1, 1)
    y = spot_returns.values
    
    model.fit(X, y)
    beta = model.coef_[0]
    r_squared = model.score(X, y)
    
    return beta, r_squared

# Example Usage
# portfolio_returns = ...
# index_futures_returns = ...
# h, r2 = optimal_hedge_ratio(portfolio_returns, index_futures_returns)
# print(f"Optimal Hedge Ratio: {h:.2f}")
# print(f"Hedging Efficiency (R^2): {r2:.2%}")
```

---

## Related Notes
- [[Strategies MOC]] — Master navigation
- [[Greeks Deep Dive]] — The mathematics of Delta/Gamma
- [[Volatility Surface Modeling]] — Pricing the hedge instruments
- [[Portfolio Optimization]] — Minimizing portfolio variance
- [[Risk Management MOC]] — Broader risk concepts
