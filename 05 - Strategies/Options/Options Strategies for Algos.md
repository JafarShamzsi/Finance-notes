# Options Strategies for Algos

**Core Idea:** Options provide non-linear payoffs, allowing you to trade volatility, hedge positions, and express complex views algorithmically.

---

## Options Fundamentals

### The Greeks
| Greek | Measures | Formula (Black-Scholes) |
|---|---|---|
| **Delta (Δ)** | Price sensitivity to underlying | ∂V/∂S = N(d₁) for calls |
| **Gamma (Γ)** | Rate of change of delta | ∂²V/∂S² |
| **Theta (Θ)** | Time decay (cost of holding) | ∂V/∂t |
| **Vega (ν)** | Sensitivity to implied volatility | ∂V/∂σ |
| **Rho (ρ)** | Sensitivity to interest rates | ∂V/∂r |

### Black-Scholes Formula
```
Call = S·N(d₁) - K·e^(-rT)·N(d₂)
Put  = K·e^(-rT)·N(-d₂) - S·N(-d₁)

d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ - σ√T
```

```python
from scipy.stats import norm
import numpy as np

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    else:
        price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = -(S * norm.pdf(d1) * sigma) / (2*np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)

    return {'price': price, 'delta': delta, 'gamma': gamma,
            'theta': theta, 'vega': vega}
```

## Algorithmic Options Strategies

### 1. Volatility Arbitrage
Trade the difference between **implied** and **realized** volatility.

```
If IV > Realized Vol → Sell options (collect premium)
If IV < Realized Vol → Buy options (cheap insurance)
```

```python
def vol_arb_signal(iv_series, rv_series, threshold=0.05):
    """
    iv_series: Implied volatility
    rv_series: Realized volatility (e.g., 20-day)
    """
    spread = iv_series - rv_series

    signal = pd.Series(0, index=spread.index)
    signal[spread > threshold] = -1   # Sell vol (straddles/strangles)
    signal[spread < -threshold] = 1   # Buy vol
    return signal
```

### 2. Delta-Neutral Trading
Isolate volatility exposure by hedging directional risk.

```python
def delta_hedge(option_delta, shares_held, underlying_price):
    """
    Maintain delta-neutral portfolio.
    """
    total_delta = option_delta * 100  # Options are per 100 shares
    hedge_shares = -total_delta - shares_held
    return hedge_shares  # Shares to buy/sell
```

### 3. Theta Harvesting (Wheel Strategy)
Systematically sell options and collect premium:
1. Sell cash-secured puts on stocks you'd buy
2. If assigned, sell covered calls on the position
3. Repeat — collect theta

```python
def wheel_strategy_signal(price, support, resistance, iv_rank):
    """
    Sell puts near support, calls near resistance.
    Only sell when IV is high (IV rank > 50%).
    """
    if iv_rank > 0.5:
        if price <= support * 1.05:
            return 'SELL_PUT', support * 0.95  # Strike below support
        elif price >= resistance * 0.95:
            return 'SELL_CALL', resistance * 1.05  # Strike above resistance
    return 'WAIT', None
```

### 4. Dispersion Trading
Sell index options, buy component stock options.
- Correlation risk premium — index vol tends to be overpriced
- Profit when realized correlation < implied correlation

### 5. Skew Trading
Trade the shape of the volatility surface:
- Put skew typically steep (crash protection demand)
- Sell expensive OTM puts, buy cheap OTM calls (risk reversal)

## IV Rank and IV Percentile

```python
def iv_rank(current_iv, iv_52w_high, iv_52w_low):
    """Where is current IV relative to past year?"""
    return (current_iv - iv_52w_low) / (iv_52w_high - iv_52w_low)

def iv_percentile(current_iv, iv_history_1y):
    """What % of days had lower IV?"""
    return (iv_history_1y < current_iv).mean()
```

- IV Rank > 50%: Favor selling premium
- IV Rank < 30%: Favor buying options (cheap)

## Key Structures

| Strategy | View | Max Profit | Max Loss |
|---|---|---|---|
| **Straddle** (buy call+put) | High volatility expected | Unlimited | Premium paid |
| **Iron Condor** | Range-bound | Premium collected | Width - premium |
| **Vertical Spread** | Directional with defined risk | Width - premium | Premium paid |
| **Calendar Spread** | Near-term vol < far-term | Complex | Premium paid |
| **Butterfly** | Pin to strike | Width - premium | Premium paid |

---

**Related:** [[Probability and Statistics for Trading]] | [[Stochastic Calculus]] | [[Risk Management MOC]] | [[Strategies MOC]]
