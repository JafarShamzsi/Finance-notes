# Correlation and Diversification

**Diversification** is often called the "only free lunch in finance." By combining assets that are not perfectly correlated, a quant can achieve a higher return per unit of risk (Sharpe Ratio) than any individual asset.

---

## 1. Linear Correlation ($\rho$)

Pearson correlation measures the degree to which two assets move together.
$$\rho_{X,Y} = \frac{Cov(X,Y)}{\sigma_X \sigma_Y}$$

- **+1.0:** Perfect positive correlation (No diversification).
- **0.0:** No linear relationship (Excellent diversification).
- **-1.0:** Perfect negative correlation (Hedging).

---

## 2. The Power of Diversification

The risk of a portfolio of $N$ assets is:
$$\sigma_p^2 = \sum w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j \rho_{ij} \sigma_i \sigma_j$$

**Key Insight:** As $N$ increases, the "Asset-Specific Risk" (idiosyncratic) is diversified away, leaving only the "Market Risk" (systematic).

---

## 3. The Correlation Breakdown (Crisis)

In a market crash, **"all correlations go to 1."**
- **The Problem:** Assets that look uncorrelated during normal times (e.g., Equities and High-Yield Bonds) tend to crash together during liquidity crises.
- **Quant Mitigation:** Use [[Copulas]] to model "Tail Dependence" instead of just linear correlation.

---

## 4. Measuring Diversification Quality

### A. Diversification Ratio (DR)
$$\text{DR} = \frac{\sum w_i \sigma_i}{\sigma_p}$$
- $\text{DR} > 1$ implies a diversification benefit.

### B. Number of Effective Bets
$$\text{Effective Bets} = \frac{(\sum \sigma_i)^2}{\sum \sum \rho_{ij} \sigma_i \sigma_j}$$
- Tells you how many "independent" return streams you actually have.

---

## 5. Implementation for Quants

- **Avoid Cluster Risk:** Don't just diversify by "Asset Name." Use [[Principal Component Analysis (PCA)]] to ensure your assets aren't all exposed to the same underlying factor (e.g., "The Fed Pivot").
- **Dynamic Correlation:** Correlations are non-stationary. Use [[Kalman Filter]] or DCC-GARCH models to track how relationships change in real-time.

---

## Related Notes
- [[Risk Management MOC]] — Broader safety context
- [[Modern Portfolio Theory]] — The math of the Efficient Frontier
- [[Copulas]] — Modeling dependency in the tails
- [[Linear Algebra in Finance]] — Matrix operations for correlation
- [[Factor Models]] — Decomposing assets into common drivers
- [[Risk Parity]] — Allocating based on risk contribution
