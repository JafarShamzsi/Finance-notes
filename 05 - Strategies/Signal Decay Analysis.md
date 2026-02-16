# Signal Decay Analysis

Every alpha signal has a lifespan. Signal decay analysis is the systematic process of measuring, monitoring, and responding to the degradation of trading signals over time. This is a critical production skill — at J.P. Morgan and every serious quant shop, alpha decay is monitored daily.

---

## Why Signals Decay

| Cause | Mechanism | Speed |
|-------|-----------|-------|
| **Crowding** | More participants discover the signal | Months-Years |
| **Data diffusion** | Alt data vendors sell to more clients | 3-12 months |
| **Regime change** | Market structure shifts (e.g., COVID, rate regime) | Sudden |
| **Technology arms race** | Faster execution erodes speed-based alpha | Ongoing |
| **Regulatory change** | New rules eliminate structural edges | Episodic |
| **Adaptive markets** | Participants learn and arbitrage away inefficiencies | Gradual |

See [[Alpha Research]] for the alpha pipeline and sources of edge.

---

## Measuring Signal Strength

### 1. Information Coefficient (IC)

The Spearman rank correlation between signal values and subsequent returns:

$$IC_t = \text{corr}(\text{signal}_t, \text{return}_{t+1})$$

```python
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

def rolling_ic(signal, forward_returns, window=63):
    """
    Compute rolling Information Coefficient.

    Parameters:
        signal: pd.DataFrame (dates × assets) of signal values
        forward_returns: pd.DataFrame of next-period returns (same shape)
        window: Rolling window in days

    Returns:
        pd.Series of rolling IC
    """
    ic_series = []
    for i in range(window, len(signal)):
        s = signal.iloc[i-window:i].values.flatten()
        r = forward_returns.iloc[i-window:i].values.flatten()
        # Remove NaN
        mask = ~(np.isnan(s) | np.isnan(r))
        if mask.sum() > 10:
            ic, _ = spearmanr(s[mask], r[mask])
            ic_series.append(ic)
        else:
            ic_series.append(np.nan)
    return pd.Series(ic_series, index=signal.index[window:])
```

### IC Interpretation
| IC Value | Strength | Typical Source |
|----------|----------|----------------|
| > 0.10 | Very strong (suspicious — check for leakage) | |
| 0.05 - 0.10 | Strong | Best signals |
| 0.02 - 0.05 | Moderate | Most live signals |
| 0.01 - 0.02 | Weak but viable (if high breadth) | Cross-sectional |
| < 0.01 | Noise | Dead signal |

### 2. IC Information Ratio (ICIR)

$$ICIR = \frac{\text{mean}(IC)}{\text{std}(IC)}$$

More stable than raw IC. A good signal has ICIR > 0.5. Decaying signals show declining ICIR.

### 3. Turnover-Adjusted Returns
```python
def turnover_adjusted_performance(signal, returns, tc_bps=5):
    """
    Compute signal returns net of turnover costs.

    Parameters:
        signal: pd.DataFrame of portfolio weights (from signal)
        returns: pd.DataFrame of asset returns
        tc_bps: Transaction cost in basis points per side
    """
    gross_returns = (signal.shift(1) * returns).sum(axis=1)
    turnover = signal.diff().abs().sum(axis=1)
    costs = turnover * tc_bps / 10000
    net_returns = gross_returns - costs
    return net_returns
```

---

## Decay Detection Framework

### Structural Break Detection
```python
def detect_signal_death(ic_series, min_periods=126, threshold=-0.5):
    """
    Detect when a signal has structurally broken.

    Uses CUSUM test on rolling IC.
    Returns the date of detected break, if any.
    """
    cumsum = (ic_series - ic_series.expanding().mean()).cumsum()

    # Detect when cumsum goes significantly negative
    rolling_std = ic_series.rolling(min_periods).std()
    z_score = cumsum / (rolling_std * np.sqrt(np.arange(1, len(cumsum)+1)))

    break_dates = z_score[z_score < threshold].index
    return break_dates[0] if len(break_dates) > 0 else None
```

### Multi-Metric Dashboard
```python
class SignalMonitor:
    """
    Production signal monitoring system.
    Run daily to track signal health.
    """

    def __init__(self, signal, forward_returns, lookback=252):
        self.signal = signal
        self.returns = forward_returns
        self.lookback = lookback

    def health_report(self):
        """Generate daily signal health report."""
        ic = rolling_ic(self.signal, self.returns, window=63)

        report = {
            'ic_current': ic.iloc[-1] if len(ic) > 0 else np.nan,
            'ic_3m_avg': ic.iloc[-63:].mean() if len(ic) >= 63 else np.nan,
            'ic_12m_avg': ic.iloc[-252:].mean() if len(ic) >= 252 else np.nan,
            'icir_3m': ic.iloc[-63:].mean() / ic.iloc[-63:].std() if len(ic) >= 63 else np.nan,
            'ic_trend': self._ic_trend(ic),
            'hit_rate': self._hit_rate(),
            'pnl_drawdown': self._current_drawdown(),
            'status': self._signal_status(ic),
        }
        return report

    def _ic_trend(self, ic, short=63, long=252):
        """Is IC trending up or down?"""
        if len(ic) < long:
            return 'insufficient_data'
        short_ic = ic.iloc[-short:].mean()
        long_ic = ic.iloc[-long:].mean()
        if short_ic > long_ic * 1.2:
            return 'improving'
        elif short_ic < long_ic * 0.5:
            return 'decaying'
        return 'stable'

    def _hit_rate(self):
        """Fraction of periods where signal direction was correct."""
        sig_direction = np.sign(self.signal)
        ret_direction = np.sign(self.returns)
        correct = (sig_direction == ret_direction).mean()
        return correct.mean() if hasattr(correct, 'mean') else correct

    def _current_drawdown(self):
        """Current P&L drawdown from peak."""
        pnl = (self.signal.shift(1) * self.returns).sum(axis=1).cumsum()
        peak = pnl.expanding().max()
        dd = (pnl - peak) / peak.replace(0, np.nan)
        return dd.iloc[-1] if len(dd) > 0 else 0

    def _signal_status(self, ic):
        """Traffic light status."""
        recent_ic = ic.iloc[-63:].mean() if len(ic) >= 63 else 0
        if recent_ic > 0.03:
            return 'GREEN'
        elif recent_ic > 0.01:
            return 'YELLOW'
        else:
            return 'RED'
```

---

## Response Playbook

| Signal Status | IC Trend | Action |
|--------------|----------|--------|
| GREEN | Stable | Full allocation, normal monitoring |
| GREEN | Improving | Consider increasing allocation |
| YELLOW | Stable | Reduce allocation 50%, investigate |
| YELLOW | Decaying | Reduce to 25%, start replacement research |
| RED | Any | Cut to 0 or minimum, find replacement |

### Capital Reallocation
```python
def dynamic_signal_allocation(signals_health, total_capital):
    """
    Allocate capital across signals based on health scores.

    Parameters:
        signals_health: dict of {signal_name: health_report}
        total_capital: Total capital to allocate
    """
    weights = {}
    for name, report in signals_health.items():
        if report['status'] == 'GREEN':
            w = 1.0
        elif report['status'] == 'YELLOW':
            w = 0.5
        else:
            w = 0.0

        # Adjust by ICIR
        icir = report.get('icir_3m', 0)
        w *= max(0, min(2, icir))
        weights[name] = w

    # Normalize
    total_w = sum(weights.values())
    if total_w > 0:
        weights = {k: v / total_w * total_capital for k, v in weights.items()}
    return weights
```

---

## Signal Half-Life Estimation

$$\text{Half-life} = -\frac{\ln(2)}{\lambda}$$

Where $\lambda$ is the decay rate estimated from exponential fit to rolling IC:

```python
def estimate_signal_halflife(ic_series):
    """
    Estimate signal half-life by fitting exponential decay to IC.
    """
    from scipy.optimize import curve_fit

    # Remove NaN
    ic_clean = ic_series.dropna()
    t = np.arange(len(ic_clean))

    def exp_decay(t, a, lam):
        return a * np.exp(-lam * t)

    try:
        popt, _ = curve_fit(exp_decay, t, ic_clean.values, p0=[0.05, 0.001],
                            maxfev=5000)
        a, lam = popt
        half_life = np.log(2) / lam if lam > 0 else np.inf
        return half_life  # In days
    except:
        return np.inf
```

---

## Related Notes
- [[Alpha Research]] — Alpha pipeline and signal construction
- [[Factor Investing]] — Factor decay and crowding
- [[Performance Metrics]] — Sharpe, IC, and other measures
- [[Overfitting]] — False signals that "decay" were never real
- [[Walk-Forward Analysis]] — Out-of-sample signal validation
- [[Machine Learning Strategies]] — ML model decay
- [[Strategies MOC]] — Strategy implementations
- [[Risk Management MOC]] — Position sizing during decay
