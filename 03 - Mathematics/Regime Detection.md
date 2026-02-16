# Regime Detection

Markets alternate between distinct regimes (bull, bear, high-vol, low-vol, trending, mean-reverting). Detecting the current regime is critical for strategy selection and risk management.

---

## Why Regime Detection Matters

The same strategy performs drastically differently across regimes:

| Strategy | Bull/Low-Vol | Bear/High-Vol | Sideways |
|----------|-------------|---------------|----------|
| Momentum | Excellent | Terrible (crashes) | Poor |
| Mean reversion | Good | Dangerous | Excellent |
| Market making | Good | Risky (spreads widen) | Excellent |
| Risk parity | Good | Drawdowns (correlation spike) | Good |

**Without regime detection, you're running strategies blind.**

---

## Method 1: Hidden Markov Model (HMM)

The gold standard for regime detection. Assumes markets switch between $K$ hidden states, each with different return distributions.

### Model

$$P(R_t | S_t = k) = \mathcal{N}(\mu_k, \sigma_k^2)$$

Where:
- $S_t \in \{1, 2, ..., K\}$ is the hidden state at time $t$
- Each state has its own mean return $\mu_k$ and volatility $\sigma_k$
- Transition matrix $A_{ij} = P(S_{t+1} = j | S_t = i)$

```python
import numpy as np
from hmmlearn.hmm import GaussianHMM

class RegimeDetector:
    def __init__(self, n_regimes=2, n_iter=100):
        self.model = GaussianHMM(
            n_components=n_regimes,
            covariance_type="full",
            n_iter=n_iter,
            random_state=42
        )

    def fit(self, returns):
        """
        Fit HMM to return series.

        Parameters:
            returns: Array of returns (T,) or (T, n_features)
        """
        if returns.ndim == 1:
            returns = returns.reshape(-1, 1)
        self.model.fit(returns)
        return self

    def predict(self, returns):
        """Predict regime for each time step."""
        if returns.ndim == 1:
            returns = returns.reshape(-1, 1)
        return self.model.predict(returns)

    def predict_proba(self, returns):
        """Get probability of each regime at each time step."""
        if returns.ndim == 1:
            returns = returns.reshape(-1, 1)
        return self.model.predict_proba(returns)

    def regime_stats(self, returns, regimes):
        """Compute statistics for each regime."""
        stats = {}
        for k in range(self.model.n_components):
            mask = regimes == k
            regime_rets = returns[mask]
            stats[k] = {
                'mean': np.mean(regime_rets) * 252,  # Annualized
                'vol': np.std(regime_rets) * np.sqrt(252),
                'sharpe': np.mean(regime_rets) / np.std(regime_rets) * np.sqrt(252),
                'pct_time': np.sum(mask) / len(returns),
                'avg_duration': _avg_run_length(mask)
            }
        return stats


def _avg_run_length(mask):
    """Average consecutive days in regime."""
    runs = []
    count = 0
    for x in mask:
        if x:
            count += 1
        else:
            if count > 0:
                runs.append(count)
            count = 0
    if count > 0:
        runs.append(count)
    return np.mean(runs) if runs else 0
```

### Typical 2-Regime Result (S&P 500)

| Regime | Mean Return (ann.) | Volatility (ann.) | % Time | Avg Duration |
|--------|-------------------|-------------------|--------|-------------|
| **Bull/Low-Vol** | +15% | 12% | 70% | 45 days |
| **Bear/High-Vol** | -10% | 28% | 30% | 18 days |

---

## Method 2: Rolling Statistics

Simple but effective — monitor rolling volatility, correlation, and momentum.

```python
def simple_regime(returns, vol_window=60, vol_threshold=0.20):
    """
    Simple regime detection using rolling volatility.

    Returns: 'low_vol' or 'high_vol' for each period.
    """
    rolling_vol = returns.rolling(vol_window).std() * np.sqrt(252)
    regimes = np.where(rolling_vol > vol_threshold, 'high_vol', 'low_vol')
    return regimes
```

---

## Method 3: Change Point Detection

Detect structural breaks in the data (mean or variance shifts).

**Algorithms:**
- **CUSUM** — Cumulative sum test for mean shifts
- **PELT** — Pruned Exact Linear Time for multiple change points
- **Bayesian Online Change Point Detection** — Real-time detection

---

## Strategy Adaptation by Regime

```python
def regime_adaptive_strategy(returns, signals_momentum, signals_mean_rev, regimes):
    """
    Switch between momentum and mean reversion based on regime.
    """
    positions = np.zeros_like(returns)
    for t in range(len(returns)):
        if regimes[t] == 'trending':
            positions[t] = signals_momentum[t]
        elif regimes[t] == 'mean_reverting':
            positions[t] = signals_mean_rev[t]
        else:  # uncertain
            positions[t] = 0.5 * signals_momentum[t] + 0.5 * signals_mean_rev[t]
    return positions
```

---

## Related Notes
- [[Mathematics MOC]] — Parent section
- [[Time Series Analysis]] — Statistical foundations
- [[Momentum Strategies]] — Works in trending regimes
- [[Mean Reversion Strategies]] — Works in mean-reverting regimes
- [[Risk Management MOC]] — Regime-conditional risk limits
- [[Kalman Filter]] — Online state estimation
- [[Machine Learning Strategies]] — ML-based regime detection
