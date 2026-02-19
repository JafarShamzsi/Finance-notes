# Portfolio Management MOC

> *"Diversification is the only free lunch in finance."* — Harry Markowitz

Portfolio management is the art and science of combining assets to maximize risk-adjusted returns. For a quant, this means mathematical optimization, factor decomposition, and systematic rebalancing.

---

## Core Concepts

### Portfolio Construction
- [[Modern Portfolio Theory]] — Mean-variance optimization, efficient frontier
- [[Black-Litterman Model]] — Combining market equilibrium with views
- [[Bayesian Portfolio Optimization]] — Incorporating uncertainty and priors
- [[Factor Models]] — Decomposing returns into systematic risk factors
- [[Portfolio Optimization]] — Practical optimization beyond Markowitz

### Portfolio Maintenance
- [[Portfolio Rebalancing]] — When and how to rebalance
- [[Transaction Cost Optimization]] — Minimizing costs during rebalancing
- [[Risk Budgeting]] — Allocating risk, not just capital

### Performance
- [[Performance Attribution]] — Where did returns come from?
- [[Portfolio Performance Metrics]] — Sharpe, Sortino, Calmar, Information Ratio

---

## Key Framework: The Portfolio Construction Pipeline

```
Universe Definition → Alpha Signals → Risk Model → Optimizer → Constraints → Portfolio → Execution
       ↓                   ↓              ↓            ↓            ↓           ↓          ↓
  Asset screen      Expected returns  Covariance   Mean-var    Sector/position  Weights   TWAP/VWAP
  Liquidity filter  Factor exposures  Factor model  Risk parity  Turnover      Trades    Smart routing
```

---

## Portfolio Construction Approaches

| Approach | Method | Pros | Cons |
|----------|--------|------|------|
| **Mean-Variance** | Maximize Sharpe ratio | Theoretically optimal | Sensitive to inputs |
| **Risk Parity** | Equal risk contribution | Robust, intuitive | Ignores expected returns |
| **Black-Litterman** | Bayesian combination | Stable, intuitive | Requires views |
| **Min Variance** | Minimize portfolio vol | No alpha needed | Concentrated in low-vol |
| **Max Diversification** | Maximize diversification ratio | Robust | Complex to implement |
| **Hierarchical Risk Parity** | ML-based clustering | No inversion needed | Newer, less proven |

---

## Quick Reference Formulas

**Portfolio Return:**
$$R_p = \sum_{i=1}^{n} w_i R_i$$

**Portfolio Variance:**
$$\sigma_p^2 = \mathbf{w}^T \Sigma \mathbf{w}$$

**Sharpe Ratio:**
$$SR = \frac{R_p - R_f}{\sigma_p}$$

**Information Ratio:**
$$IR = \frac{R_p - R_b}{\sigma_{tracking}}$$

---

## Related Areas
- [[Risk Management MOC]] — Risk constraints for portfolio construction
- [[Execution MOC]] — How to implement portfolio changes
- [[Mathematics MOC]] — Optimization and linear algebra foundations
- [[Strategies MOC]] — Alpha signals that feed into portfolio construction
- [[Backtesting MOC]] — Testing portfolio strategies historically
