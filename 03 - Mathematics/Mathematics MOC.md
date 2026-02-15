# Mathematics — Map of Content

> The mathematical foundations that underpin every quantitative trading strategy.

---

## Core Areas

### Probability & Statistics → [[Probability and Statistics for Trading]]
- Distributions (Normal, Log-Normal, Fat-Tailed)
- Hypothesis testing for strategy validation
- Bayesian inference for dynamic models
- Regression analysis

### Time Series Analysis → [[Time Series Analysis]]
- Stationarity and unit root tests
- ARIMA, GARCH models
- Cointegration (Engle-Granger, Johansen)
- Regime switching models

### Stochastic Calculus → [[Stochastic Calculus]]
- Brownian motion and Wiener process
- Itô's lemma
- Geometric Brownian Motion (GBM)
- Stochastic differential equations
- Black-Scholes derivation

### Linear Algebra → [[Linear Algebra in Finance]]
- Covariance matrices
- Principal Component Analysis (PCA)
- Matrix operations for portfolio optimization
- Eigenvalue decomposition

### Optimization → [[Optimization Methods]]
- Convex optimization (portfolio construction)
- Gradient descent (ML model training)
- Dynamic programming
- Genetic algorithms for strategy optimization

### Simulation → [[Monte Carlo Simulation]]
- Random number generation
- Path simulation for derivatives pricing
- Risk estimation via simulation
- Bootstrap methods

### Filtering → [[Kalman Filter]]
- State estimation from noisy observations
- Dynamic hedge ratios
- Pairs trading spread estimation

## Quick Reference: Key Formulas

### Returns
```
Simple Return:      R = (P_t - P_{t-1}) / P_{t-1}
Log Return:         r = ln(P_t / P_{t-1})
Annualized Return:  R_a = (1 + R_daily)^252 - 1
```

### Risk
```
Volatility:         σ = std(returns) × √252
Sharpe Ratio:       SR = (R - Rf) / σ
Sortino Ratio:      So = (R - Rf) / σ_downside
Max Drawdown:       MDD = max(peak - trough) / peak
```

### Correlation
```
Correlation:        ρ = Cov(X,Y) / (σ_X × σ_Y)
Beta:               β = Cov(R_i, R_m) / Var(R_m)
```

---

**Related:** [[Trading Algorithms Master Index]] | [[Strategies MOC]] | [[Risk Management MOC]] | [[Backtesting MOC]]
