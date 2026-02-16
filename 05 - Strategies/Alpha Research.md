# Alpha Research

Alpha is excess return above a benchmark after adjusting for risk. Alpha research is the systematic process of discovering, testing, and deploying trading signals. This is the core job of a quant.

---

## The Alpha Pipeline

```
Idea Generation → Data Collection → Feature Engineering → Signal Construction →
     ↓                   ↓                  ↓                    ↓
  Literature        Market data         Transforms          Combine features
  Intuition         Alt data            Normalization       into a score
  Observation       Fundamentals        Cross-sectional
                                        Time-series

→ Backtesting → Statistical Testing → Paper Trading → Live Deployment → Monitoring
       ↓               ↓                   ↓                ↓              ↓
   Walk-forward    Multiple testing    Sim with real     Gradual         Signal decay
   Out-of-sample   correction          data feed         ramp-up         tracking
```

---

## Where Alpha Comes From

### Sources of Edge

| Source | Example | Decay Speed | Competition |
|--------|---------|-------------|-------------|
| **Speed** | Latency arbitrage, news reaction | Seconds | Extreme (HFT) |
| **Data** | Alternative data (satellite, credit card) | Months | Growing |
| **Model** | Better ML model, novel features | Months-Years | Medium |
| **Behavioral** | Overreaction, anchoring, herding | Years | Low |
| **Structural** | Index rebalancing, forced selling | Persistent | Medium |
| **Risk premia** | Value, momentum, carry | Persistent | Variable |

### The Fundamental Law of Active Management (Grinold, 1989)

$$IR = IC \times \sqrt{BR}$$

Where:
- **IR** = Information Ratio (alpha / tracking error)
- **IC** = Information Coefficient (correlation between predicted and actual returns)
- **BR** = Breadth (number of independent bets per year)

**Implications:**
- A small IC (e.g., 0.05) can generate a good IR if breadth is high (many stocks, frequent trading)
- Better to be slightly right on many stocks than very right on a few
- Cross-sectional strategies (many stocks) have higher BR than time-series (one asset)

---

## Signal Construction

### Z-Score Normalization
```python
def zscore_signal(raw_signal, window=252):
    """
    Normalize signal to z-score (cross-sectionally or time-series).
    Ensures signal has mean 0, std 1 — comparable across assets.
    """
    rolling_mean = raw_signal.rolling(window).mean()
    rolling_std = raw_signal.rolling(window).std()
    return (raw_signal - rolling_mean) / rolling_std
```

### Signal Combination
Multiple weak signals combined are stronger than any individual signal:

```python
def combine_signals(signals, weights=None):
    """
    Combine multiple alpha signals.

    Parameters:
        signals: dict of {name: pd.DataFrame} — each signal is z-scored
        weights: dict of {name: float} — signal weights (default: equal)
    """
    if weights is None:
        weights = {name: 1.0 / len(signals) for name in signals}

    combined = sum(signals[name] * weights[name] for name in signals)
    # Re-normalize
    return (combined - combined.mean()) / combined.std()
```

---

## Alpha Decay

Every alpha signal decays over time as more participants discover and trade it.

| Alpha Type | Typical Half-Life | Why It Decays |
|------------|------------------|---------------|
| Speed-based | Days-Weeks | Technology arms race |
| Data-based | 3-12 months | Data vendors sell to more clients |
| Behavioral | Years | Human nature changes slowly |
| Structural | Persistent | Regulatory/institutional constraints |
| Risk premia | Persistent (cyclical) | Compensation for bearing risk |

### Monitoring Alpha Decay
```python
def rolling_ic(signal, forward_returns, window=63):
    """
    Track Information Coefficient over time.
    Declining IC = alpha decay.
    """
    ic_series = signal.rolling(window).corr(forward_returns)
    return ic_series
```

**Action when alpha decays:**
1. Reduce position size proportionally
2. Search for new uncorrelated signals
3. Move to less competitive markets/timeframes

---

## WorldQuant-Style Formulaic Alphas

Igor Tulchinsky's "101 Formulaic Alphas" paper — simple signals that work cross-sectionally:

```python
# Alpha #1: (rank(Ts_ArgMax(SignedPower(returns, 2), 5)) - 0.5)
# Alpha #6: -correlation(open, volume, 10)
# Alpha #12: sign(delta(volume, 1)) * (-delta(close, 1))

def alpha_momentum_volume(close, volume, lookback=20):
    """Price momentum weighted by volume change."""
    price_mom = close.pct_change(lookback)
    vol_change = volume / volume.rolling(lookback).mean()
    raw = price_mom * vol_change
    return raw.rank(axis=1, pct=True) - 0.5  # Cross-sectional rank
```

---

## Testing for Statistical Significance

### Multiple Testing Problem
If you test 1000 signals at 5% significance, you expect 50 false positives.

**Corrections:**
- **Bonferroni:** Divide alpha by number of tests ($\alpha / N$). Conservative.
- **Holm-Bonferroni:** Sequential rejection. Less conservative.
- **Benjamini-Hochberg (FDR):** Controls false discovery rate. Preferred in practice.
- **Deflated Sharpe Ratio (López de Prado):** Accounts for number of trials to find a strategy.

```python
def deflated_sharpe(observed_sharpe, n_trials, T, skew=0, kurtosis=3):
    """
    Deflated Sharpe Ratio (López de Prado).
    Probability that the observed Sharpe is genuine given N trials.
    """
    from scipy.stats import norm
    # Expected max Sharpe under null
    e_max_sr = norm.ppf(1 - 1/n_trials) * np.sqrt(1/T)
    # Standard error of Sharpe
    se_sr = np.sqrt((1 + 0.5 * observed_sharpe**2 -
                     skew * observed_sharpe +
                     (kurtosis - 3) / 4 * observed_sharpe**2) / T)
    # Probability Sharpe is genuine
    return norm.cdf((observed_sharpe - e_max_sr) / se_sr)
```

---

## Related Notes
- [[Strategies MOC]] — Strategy implementations
- [[Factor Models]] — Factor-based alpha
- [[Machine Learning Strategies]] — ML alpha signals
- [[Feature Engineering for Trading]] — Feature construction
- [[Overfitting]] — Avoiding false alpha
- [[Backtesting MOC]] — Testing alpha
- [[Performance Attribution]] — Measuring alpha sources
- [[Key Papers]] — Foundational alpha research
