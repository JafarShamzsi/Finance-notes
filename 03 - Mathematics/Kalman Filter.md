# Kalman Filter

An optimal recursive algorithm for estimating the state of a dynamic system from noisy observations. In trading, used for adaptive parameter estimation.

---

## Core Concept

```
Hidden State (what we want):  x_t = A·x_{t-1} + w_t   (state transition)
Observation (what we see):    z_t = H·x_t + v_t        (measurement)

w_t ~ N(0, Q)  process noise
v_t ~ N(0, R)  measurement noise
```

**Two steps each iteration:**
1. **Predict** — Estimate next state from model
2. **Update** — Correct estimate with new observation

## Applications in Trading

### 1. Dynamic Hedge Ratio for [[Pairs Trading]]
```python
from pykalman import KalmanFilter
import numpy as np

def kalman_pairs_trading(price_y, price_x):
    """
    Estimate time-varying hedge ratio using Kalman filter.
    State: [hedge_ratio, intercept]
    Observation: price_y = hedge_ratio * price_x + intercept
    """
    delta = 1e-5
    n = len(price_y)

    # State: [beta, alpha]
    trans_cov = delta / (1 - delta) * np.eye(2)

    obs_mat = np.vstack([price_x, np.ones(n)]).T[:, np.newaxis, :]

    kf = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=np.zeros(2),
        initial_state_covariance=np.eye(2),
        transition_matrices=np.eye(2),
        observation_matrices=obs_mat,
        observation_covariance=1.0,
        transition_covariance=trans_cov
    )

    state_means, state_covs = kf.filter(price_y)

    hedge_ratios = state_means[:, 0]
    intercepts = state_means[:, 1]
    spread = price_y - hedge_ratios * price_x - intercepts

    return hedge_ratios, intercepts, spread
```

### 2. Trend Estimation (Noise Reduction)
```python
def kalman_trend_filter(prices, observation_noise=1.0, process_noise=0.01):
    """
    Extract smooth trend from noisy price data.
    Better than moving averages — less lag.
    """
    kf = KalmanFilter(
        initial_state_mean=prices.iloc[0],
        initial_state_covariance=1.0,
        transition_matrices=[1],
        observation_matrices=[1],
        observation_covariance=observation_noise,
        transition_covariance=process_noise
    )

    filtered_state, _ = kf.filter(prices.values)
    return pd.Series(filtered_state.flatten(), index=prices.index)
```

### 3. Dynamic Beta Estimation
Track time-varying market beta:
```python
def kalman_beta(asset_returns, market_returns):
    """Estimate time-varying CAPM beta."""
    # State: [beta, alpha], Observation: R_i = alpha + beta * R_m
    obs_mat = np.column_stack([market_returns, np.ones(len(market_returns))])
    obs_mat = obs_mat[:, np.newaxis, :]

    kf = KalmanFilter(
        n_dim_obs=1, n_dim_state=2,
        initial_state_mean=[1, 0],
        initial_state_covariance=np.eye(2),
        transition_matrices=np.eye(2),
        observation_matrices=obs_mat,
        observation_covariance=0.01,
        transition_covariance=1e-5 * np.eye(2)
    )

    state_means, _ = kf.filter(asset_returns)
    return state_means[:, 0]  # Time-varying beta
```

## Advantages Over Moving Averages

| Property | Moving Average | Kalman Filter |
|---|---|---|
| Lag | Fixed, proportional to window | Minimal, adaptive |
| Parameters | Window size | Process/observation noise |
| Optimality | Heuristic | Optimal (for Gaussian systems) |
| Adaptiveness | Fixed | Automatically adjusts |

---

**Related:** [[Mathematics MOC]] | [[Pairs Trading]] | [[Statistical Arbitrage]] | [[Time Series Analysis]] | [[Feature Engineering for Trading]]
