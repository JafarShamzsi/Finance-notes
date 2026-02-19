# Market Impact Models

Market impact is the change in asset price caused by a trade. It is the primary cost for large institutional orders, often exceeding commissions and spreads by orders of magnitude.

Understanding impact is crucial for:
1.  **Optimal Execution:** Minimizing implementation shortfall.
2.  **Capacity Constraints:** Determining the maximum AUM a strategy can handle.
3.  **Alpha Decay:** Why profitable signals disappear once traded.

---

## 1. Components of Impact

### Temporary Impact (Liquidity Cost)
- Caused by consuming liquidity at the best bid/ask and walking the book.
- **Reverts:** The price bounces back once the liquidity is replenished.
- **Cost:** Paid by the aggressive trader to liquidity providers.

### Permanent Impact (Information Leakage)
- Caused by the market inferring information from the trade flow.
- **Persists:** The price moves to a new equilibrium level and stays there.
- **Cost:** Reduces the profitability of the remaining order (adverse selection).

---

## 2. The Square Root Law

Empirical studies (e.g., Torre 1997, Almgren et al. 2005) consistently show that market impact is proportional to the square root of the trade size relative to daily volume.

$$I = \sigma \cdot \left( \frac{Q}{V} \right)^{0.5}$$

Where:
- $I$: Price impact (in basis points)
- $\sigma$: Daily volatility
- $Q$: Order size
- $V$: Average Daily Volume (ADV)

---

## 3. Almgren-Chriss Model (2000)

The seminal framework for optimal execution. It balances **Execution Cost** (impact) vs. **Market Risk** (volatility).

### Objective Function
Minimize: $\mathbb{E}[C] + \lambda \mathbb{V}[C]$

- **Expected Cost ($\mathbb{E}[C]$):** Driven by market impact. Trading *slower* reduces impact.
- **Risk ($\mathbb{V}[C]$):** Driven by price volatility. Trading *faster* reduces exposure to market moves.

### The Solution: Trajectory
The optimal trading schedule depends on the risk aversion parameter $\lambda$.
- **Risk Neutral ($\lambda = 0$):** Trade very slowly (TWAP-like) to minimize impact.
- **Risk Averse ($\lambda > 0$):** Trade faster (Front-loaded) to reduce risk.

### Mathematical Formulation
$$x_k = X \frac{\sinh(\kappa(T - t_k))}{\sinh(\kappa T)}$$
Where $\kappa$ is a parameter derived from volatility and impact coefficients.

---

## 4. Decay Kernels (Propagator Models)

Impact is dynamic. A trade at time $t$ impacts prices at time $t+\tau$, but the effect decays.

$$P_t = P_0 + \int_0^t G(t - s) \cdot \dot{x}_s ds + \text{Noise}$$

- $G(\tau)$: The **Decay Kernel** (Propagator). Typically a power law $G(\tau) \sim \tau^{-\beta}$.
- $\dot{x}_s$: Trading rate at time $s$.

This model explains why impact accumulates during a meta-order and decays (reverts) after it finishes.

---

## Python Implementation: Simple Impact Estimator

```python
import numpy as np

def estimate_impact(shares, adv, volatility, spread, model='sqrt'):
    """
    Estimate market impact cost in basis points.
    
    Parameters:
        shares: Order size
        adv: Average Daily Volume
        volatility: Daily volatility (decimal, e.g., 0.02)
        spread: Bid-Ask spread (decimal, e.g., 0.0005)
    """
    participation_rate = shares / adv
    
    if model == 'sqrt':
        # Classic Square Root Law (with a typical coefficient of 0.5-1.0)
        # Impact (bps) ~ Vol * sqrt(PartRate)
        impact_bps = 1.0 * volatility * np.sqrt(participation_rate) * 10000
        
    elif model == 'linear':
        # Temporary impact often modeled as linear for small trades
        # Impact ~ Spread/2 + Linear term
        impact_bps = (spread / 2 + 0.1 * participation_rate) * 10000
        
    return impact_bps

# Example
shares = 50000
adv = 1000000  # 5% participation
vol = 0.02     # 2% daily vol
spread = 0.001 # 10bps spread

cost = estimate_impact(shares, adv, vol, spread)
print(f"Estimated Impact Cost: {cost:.2f} bps")
```

---

## Related Notes
- [[Execution MOC]] — Master navigation
- [[Transaction Cost Analysis (TCA)]] — Measuring realized impact
- [[Liquidity]] — The source of impact
- [[Order Book Dynamics]] — Microstructure details
- [[VWAP Algorithm]] — Typical execution benchmark
