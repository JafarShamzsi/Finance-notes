# FX Trading Strategies

The Foreign Exchange (Forex) market is the largest financial market in the world, with daily turnover exceeding $7.5 trillion. Unlike equities, FX is traded Over-The-Counter (OTC) and operates 24/5.

Strategies in FX are driven by **macroeconomic flows**, **interest rate differentials**, and **central bank policies**.

---

## 1. Market Structure

- **G10 Currencies:** USD, EUR, JPY, GBP, AUD, CAD, CHF, NZD, SEK, NOK. Highly liquid, tight spreads.
- **Emerging Markets (EM):** MXN, BRL, ZAR, TRY, CNY. Higher volatility, higher interest rates (carry), often subject to capital controls.
- **Crosses:** Pairs not involving USD (e.g., EUR/JPY, AUD/NZD).

---

## 2. The Carry Trade

The most famous FX strategy. Borrow in a low-interest-rate currency (Funding Currency) and invest in a high-interest-rate currency (Target Currency).

### The Logic
$$R_{total} \approx (i_{high} - i_{low}) + \Delta S$$

- **Interest Rate Differential $(i_{high} - i_{low})$:** The "carry" earned daily.
- **Spot Return $(\Delta S)$:** Ideally stable or appreciating.
- **Risk:** Uncovered Interest Parity (UIP) says the high-yielding currency *should* depreciate to offset the yield advantage. Empirically, it often *doesn't* (the "Forward Premium Puzzle"), making carry profitable.

### Risks
- **"Crash Risk":** Carry trades are like "picking up pennies in front of a steamroller." When risk sentiment sours (risk-off), high-beta currencies (AUD, EM) crash against funding currencies (JPY, USD).
- **Liquidity Spirals:** Unwinds can be violent as everyone exits simultaneously.

---

## 3. FX Momentum & Trend Following

Currencies trend due to long-lasting economic cycles and central bank policy divergences.

### Drivers
- **Central Bank Divergence:** If the Fed is hiking and the BOJ is easing, USD/JPY trends up for months/years.
- **Terms of Trade:** Commodity prices drive commodity currencies (AUD, CAD, NZD).
- **Current Account Balances:** Structural deficits/surpluses drive long-term valuation.

### Implementation
- **Time Series Momentum:** Trend following on individual pairs (e.g., long EUR/USD if > 200 SMA).
- **Cross-Sectional Momentum:** Buy the strongest 3 currencies against the weakest 3.

---

## 4. Valuation Models (Mean Reversion)

- **Purchasing Power Parity (PPP):** The "Big Mac Index" theory. In the long run, exchange rates should equalize the price of a basket of goods.
  - Used for long-term horizons (years).
- **Real Effective Exchange Rate (REER):** Trade-weighted average exchange rate adjusted for inflation.
  - Deviation from historical average REER signals over/undervaluation.

---

## 5. Volatility Strategies in FX

FX volatility has a unique structure.
- **Smile:** Always present in FX options (unlike equities which have a skew).
- **Straddles:** Buying volatility ahead of major central bank announcements (FOMC, ECB) or Non-Farm Payrolls (NFP).
- **Risk Reversals:** Trading the skew (Call Vol - Put Vol) to express directional views.

---

## Python Implementation: Simple Carry Signal

```python
import pandas as pd

def compute_carry_signal(spot_prices, interest_rates):
    """
    Compute carry trade signal based on interest rate differentials.
    
    Parameters:
        spot_prices: DataFrame of currency pairs (e.g., USDJPY, AUDUSD)
        interest_rates: DataFrame of central bank rates (e.g., US, JP, AU)
    """
    # Calculate differentials (simplified example)
    # Long AUD/JPY = Long AUD (High Yield) + Short JPY (Low Yield)
    
    carry = interest_rates['AUD'] - interest_rates['JPY']
    
    signal = 1 if carry > 0.02 else 0 # Enter if diff > 2%
    
    return signal, carry

# Example
rates = {'USD': 0.0525, 'JPY': -0.001, 'AUD': 0.041, 'EUR': 0.04}
print(f"USD/JPY Carry: {rates['USD'] - rates['JPY']:.2%}")
print(f"AUD/JPY Carry: {rates['AUD'] - rates['JPY']:.2%}")
# Result: Both positive carry trades
```

---

## Related Notes
- [[Strategies MOC]] — Master navigation
- [[Macro Economics]] — (To be created) Drivers of rates
- [[Fixed Income]] — Interest rate models drive FX
- [[Volatility Surface Modeling]] — FX smiles
- [[Risk Parity]] — Often includes FX carry as an asset class
