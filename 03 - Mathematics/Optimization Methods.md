# Optimization Methods

Optimization is used everywhere in quant trading: portfolio construction, strategy parameter tuning, execution, and ML training.

---

## Portfolio Optimization

### Convex Optimization (Markowitz)
```python
import cvxpy as cp

def optimize_portfolio(expected_returns, cov_matrix, risk_aversion=1.0):
    """
    Mean-variance optimization using CVXPY.

    max: w'μ - (λ/2)w'Σw
    s.t.: Σw = 1, w ≥ 0
    """
    n = len(expected_returns)
    w = cp.Variable(n)

    ret = expected_returns @ w
    risk = cp.quad_form(w, cov_matrix)

    objective = cp.Maximize(ret - (risk_aversion / 2) * risk)
    constraints = [
        cp.sum(w) == 1,
        w >= 0,           # Long only
        w <= 0.1,         # Max 10% per asset
    ]

    prob = cp.Problem(objective, constraints)
    prob.solve()

    return w.value
```

### Risk Parity
Equal risk contribution from each asset:
```python
def risk_parity_weights(cov_matrix):
    """Each asset contributes equally to portfolio risk."""
    from scipy.optimize import minimize

    n = cov_matrix.shape[0]

    def risk_contribution_error(w):
        port_vol = np.sqrt(w @ cov_matrix @ w)
        marginal_contrib = cov_matrix @ w
        risk_contrib = w * marginal_contrib / port_vol
        target = port_vol / n
        return np.sum((risk_contrib - target)**2)

    result = minimize(risk_contribution_error, np.ones(n)/n,
                     constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                     bounds=[(0.01, 1)] * n)
    return result.x
```

## Strategy Parameter Optimization

### Grid Search
```python
def grid_search(strategy_func, param_grid, data):
    """Exhaustive search over parameter combinations."""
    results = []
    for params in itertools.product(*param_grid.values()):
        param_dict = dict(zip(param_grid.keys(), params))
        sharpe = strategy_func(data, **param_dict)
        results.append({**param_dict, 'sharpe': sharpe})
    return pd.DataFrame(results).sort_values('sharpe', ascending=False)
```

### Bayesian Optimization
More efficient than grid search for expensive evaluations:
```python
from skopt import gp_minimize

def bayesian_optimize_strategy(strategy_func, bounds, n_calls=50):
    """
    bounds: list of (low, high) for each parameter
    strategy_func should return NEGATIVE sharpe (we minimize)
    """
    result = gp_minimize(
        strategy_func,
        bounds,
        n_calls=n_calls,
        random_state=42,
        acq_func='EI'  # Expected Improvement
    )
    return result.x, -result.fun
```

**WARNING:** Optimizing parameters on the same data you test on leads to [[Overfitting and Curve Fitting]]. Always use [[Walk-Forward Analysis]].

## Gradient Descent (ML)

Used for training ML models. See [[Machine Learning Strategies]].

```python
# Adam optimizer (standard for deep learning)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Learning rate scheduling
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, patience=10, factor=0.5)
```

## Dynamic Programming

Used in [[Reinforcement Learning for Trading]] and optimal execution.

**Bellman Equation:**
```
V(s) = max_a [R(s,a) + γ·V(s')]
```

---

**Related:** [[Mathematics MOC]] | [[Portfolio Optimization]] | [[Overfitting and Curve Fitting]] | [[Walk-Forward Analysis]] | [[Machine Learning Strategies]]
