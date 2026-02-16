# Volatility Trading

Volatility trading is about taking positions on the **level or direction of volatility itself**, not on the direction of the underlying asset. This is where options really shine for quants.

---

## Core Concepts

### Implied vs. Realized Volatility
- **Implied Volatility (IV):** Market's forecast of future vol, extracted from option prices via Black-Scholes
- **Realized Volatility (RV):** Actual historical volatility computed from returns
- **Volatility Risk Premium (VRP):** IV is systematically higher than RV → selling vol is profitable on average

$$VRP = IV - RV \quad (\text{typically positive, ~2-4\% annualized})$$

### Why VRP Exists
- Option buyers pay a premium for insurance (crash protection)
- Market makers charge a premium for bearing gamma risk
- Behavioral: People overestimate tail risk (prospect theory)

---

## The Volatility Surface

Options have different IVs depending on strike and expiry. The volatility surface maps IV as a function of (strike, expiry):

```
       IV
       |
  30%  |  \                    /
  25%  |   \      ___        /     ← Volatility smile
  20%  |    \____/    \______/
  15%  |
       +----------------------------
          80%   90%  100%  110%  120%
                     Strike (% of spot)
```

### Key Features
- **Skew (Smirk):** OTM puts have higher IV than OTM calls (crash protection demand)
- **Term structure:** Short-term IV > Long-term IV in stressed markets (inverted), opposite in calm markets
- **Smile:** Both OTM puts and calls have higher IV than ATM

### Measuring Skew
```python
def skew_25d(iv_25d_put, iv_25d_call):
    """25-delta skew: standard measure of options skew."""
    return iv_25d_put - iv_25d_call

def skew_risk_reversal(iv_25d_put, iv_25d_call, iv_atm):
    """Risk reversal: normalized skew."""
    return (iv_25d_put - iv_25d_call) / iv_atm
```

---

## Volatility Trading Strategies

### 1. Variance Swap (Long/Short Vol)
Pure bet on realized vs. implied volatility. Payoff at expiry:

$$\text{Payoff} = N_{var} \times (\sigma_{realized}^2 - K_{var}^2)$$

Where $K_{var}$ is the strike (implied variance at inception).

### 2. Straddle (Long Vol)
Buy ATM call + ATM put. Profit if the underlying moves enough in either direction.

$$\text{Breakeven} = \text{Strike} \pm \text{Premium Paid}$$

### 3. Strangle (Cheaper Long Vol)
Buy OTM call + OTM put. Cheaper than straddle, needs bigger move.

### 4. Calendar Spread (Term Structure Trade)
Buy long-dated option, sell short-dated option. Bet on term structure steepening.

### 5. VIX Trading
Trade volatility directly via VIX futures and options.

| Product | Use |
|---------|-----|
| VIX futures | Direct vol exposure |
| VIX options | Options on vol (vol of vol) |
| VXX/UVXY | Long vol ETPs (decay over time) |
| SVXY | Short vol ETP (inverse VIX) |

**Warning:** Short vol strategies (selling VXX, selling puts) are profitable most of the time but have catastrophic tail risk (Volmageddon, Feb 2018: XIV lost 90%+ in one day).

---

## The Greeks for Vol Trading

| Greek | Measures | Vol Trading Relevance |
|-------|---------|---------------------|
| **Delta** | Exposure to underlying price | Hedge to zero (delta-neutral) |
| **Gamma** | Rate of delta change | Long gamma = long vol (profit from moves) |
| **Theta** | Time decay | Short gamma = collect theta |
| **Vega** | Exposure to IV change | Direct vol bet |
| **Vanna** | d(Delta)/d(Vol) | Skew exposure |
| **Volga** | d(Vega)/d(Vol) | Vol-of-vol exposure |

### Delta-Neutral Vol Trading
```
1. Buy straddle (long gamma, long vega)
2. Delta-hedge by trading the underlying
3. Profit comes from:
   - Gamma scalping: If RV > IV, delta-hedging profits exceed theta paid
   - Vega: If IV increases, option value increases
```

---

## Gamma Scalping

```python
def gamma_scalp_pnl(underlying_prices, option_gamma, delta_hedge_freq='daily'):
    """
    Estimate gamma scalping P&L.

    Gamma P&L per period ≈ 0.5 * Gamma * (ΔS)²
    Theta cost per period = Theta * Δt

    Net P&L = Gamma P&L - Theta cost
    Profitable when realized moves > implied (RV > IV)
    """
    returns = np.diff(underlying_prices) / underlying_prices[:-1]
    daily_gamma_pnl = 0.5 * option_gamma * (np.diff(underlying_prices)) ** 2
    return daily_gamma_pnl.sum()
```

---

## Practical Considerations

1. **Transaction costs are critical** — Options have wide spreads (5-20 bps)
2. **Pin risk** — Near-expiry, ATM options have explosive gamma
3. **Jump risk** — Black-Scholes assumes continuous prices; jumps break delta-hedging
4. **Correlation** — Multi-asset vol trading requires correlation modeling
5. **Margin** — Selling options requires significant margin

---

## Related Notes
- [[Options Strategies for Algos]] — Broader options strategies
- [[Stochastic Calculus]] — Black-Scholes derivation, Heston model
- [[Risk Management MOC]] — Tail risk from short vol
- [[Tail Risk and Black Swans]] — When vol trading goes wrong
- [[Strategies MOC]] — Parent strategy index
- [[Mathematics MOC]] — Greeks derivation
