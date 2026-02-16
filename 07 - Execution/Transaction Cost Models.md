# Transaction Cost Models

Transaction costs are the silent killer of alpha. A strategy that looks profitable in a frictionless backtest may lose money in production. This note covers the Almgren-Chriss framework, market impact estimation, and practical cost modeling for [[Backtesting MOC|backtesting]] and [[Execution MOC|live execution]].

---

## Components of Transaction Costs

| Component | Description | Magnitude |
|-----------|-------------|-----------|
| **Bid-ask spread** | Half-spread paid on each side | 1-50 bps |
| **Market impact** | Price movement caused by your trade | 5-100+ bps |
| **Timing cost** | Delay between decision and execution | Variable |
| **Opportunity cost** | Cost of NOT trading (signal decays) | Variable |
| **Commission** | Broker/exchange fees | 0.1-5 bps |
| **Slippage** | Execution price vs. intended price | 1-20 bps |

See [[Fees Commissions and Slippage]] for foundational concepts and [[Transaction Cost Analysis]] for post-trade measurement.

---

## Market Impact Models

### Temporary vs Permanent Impact

| Type | Definition | Cause |
|------|-----------|-------|
| **Temporary** | Price impact that reverts after trade | Liquidity displacement |
| **Permanent** | Lasting price change from information | Information content of trade |

$$\text{Total Impact} = \text{Temporary}(v) + \text{Permanent}(v)$$

Where $v$ is the trade velocity (shares per unit time).

---

## Almgren-Chriss Model (2000)

The industry-standard framework for optimal execution. Trades off **market impact** (trading fast) against **timing risk** (trading slow).

### Setup
- Sell $X$ shares over time $T$
- Divide into $N$ intervals, each of length $\tau = T/N$
- Holdings at step $k$: $x_k$, with $x_0 = X$ and $x_N = 0$
- Trade at step $k$: $n_k = x_{k-1} - x_k$, trade rate $v_k = n_k / \tau$

### Impact Functions

**Permanent impact** (per share):
$$g(v) = \gamma v$$

**Temporary impact** (per share):
$$h(v) = \epsilon \cdot \text{sign}(v) + \eta v$$

| Parameter | Meaning | How to Estimate |
|-----------|---------|----------------|
| $\gamma$ | Permanent impact coefficient | Regression on past trades |
| $\epsilon$ | Fixed cost (half-spread) | Observable from market data |
| $\eta$ | Temporary impact coefficient | Regression on execution data |

### Expected Cost and Variance

$$E[\text{cost}] = \epsilon X + \frac{\eta}{2\tau} \sum_{k=1}^{N} n_k^2 + \gamma \sum_{k=1}^{N} n_k x_{k-1}$$

$$\text{Var}[\text{cost}] = \sigma^2 \tau \sum_{k=0}^{N-1} x_k^2$$

### Optimal Trading Trajectory

The solution minimizes $E[\text{cost}] + \lambda \cdot \text{Var}[\text{cost}]$ where $\lambda$ is the risk aversion:

$$x_k = X \cdot \frac{\sinh(\kappa(T - t_k))}{\sinh(\kappa T)}$$

Where:
$$\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta / \tau}}$$

```python
import numpy as np

class AlmgrenChriss:
    """
    Almgren-Chriss optimal execution model.

    Parameters:
        X: Total shares to trade
        T: Time horizon (in days or hours)
        N: Number of time steps
        sigma: Daily volatility (in price units)
        eta: Temporary impact coefficient
        gamma: Permanent impact coefficient
        epsilon: Fixed cost (half-spread)
        risk_aversion: Lambda (risk aversion parameter)
    """

    def __init__(self, X, T, N, sigma, eta, gamma=0, epsilon=0, risk_aversion=1e-6):
        self.X = X
        self.T = T
        self.N = N
        self.tau = T / N
        self.sigma = sigma
        self.eta = eta
        self.gamma = gamma
        self.epsilon = epsilon
        self.lam = risk_aversion

        # Solve for kappa
        self.kappa = np.sqrt(self.lam * sigma**2 / (eta / self.tau))

    def optimal_trajectory(self):
        """Compute optimal holdings trajectory x_k."""
        times = np.linspace(0, self.T, self.N + 1)
        trajectory = self.X * np.sinh(self.kappa * (self.T - times)) / \
                     np.sinh(self.kappa * self.T)
        return times, trajectory

    def optimal_trades(self):
        """Compute trade sizes at each step."""
        _, trajectory = self.optimal_trajectory()
        trades = -np.diff(trajectory)  # Positive = selling
        return trades

    def expected_cost(self):
        """Expected execution cost."""
        trades = self.optimal_trades()
        _, trajectory = self.optimal_trajectory()
        holdings = trajectory[:-1]

        temp_cost = self.epsilon * abs(self.X) + \
                    (self.eta / (2 * self.tau)) * np.sum(trades**2)
        perm_cost = self.gamma * np.sum(trades * holdings)
        return temp_cost + perm_cost

    def cost_variance(self):
        """Variance of execution cost."""
        _, trajectory = self.optimal_trajectory()
        holdings = trajectory[:-1]
        return self.sigma**2 * self.tau * np.sum(holdings**2)

    def efficient_frontier(self, n_points=50):
        """
        Compute the execution efficient frontier.
        Trades off expected cost vs. cost variance.
        """
        lambdas = np.logspace(-10, -3, n_points)
        costs = []
        variances = []

        for lam in lambdas:
            model = AlmgrenChriss(self.X, self.T, self.N, self.sigma,
                                   self.eta, self.gamma, self.epsilon, lam)
            costs.append(model.expected_cost())
            variances.append(model.cost_variance())

        return np.array(costs), np.array(variances)


# --- Example ---
if __name__ == '__main__':
    # Sell 100,000 shares of a $50 stock over 1 day (6.5 hours)
    model = AlmgrenChriss(
        X=100000,        # shares
        T=1.0,           # 1 day
        N=13,            # 13 half-hour intervals
        sigma=0.50,      # $0.50 daily vol per share
        eta=0.01,        # Temporary impact
        gamma=0.001,     # Permanent impact
        epsilon=0.02,    # Half-spread ($0.02)
        risk_aversion=1e-6
    )

    times, trajectory = model.optimal_trajectory()
    trades = model.optimal_trades()

    print(f"Expected cost: ${model.expected_cost():,.2f}")
    print(f"Cost std dev:  ${np.sqrt(model.cost_variance()):,.2f}")
    print(f"\nTrading schedule:")
    for i, (t, trade) in enumerate(zip(times[:-1], trades)):
        print(f"  Period {i+1}: Trade {trade:,.0f} shares "
              f"(remaining: {trajectory[i]:,.0f})")
```

---

## Square-Root Market Impact Model

Empirical finding: market impact scales with the square root of trade size (not linearly).

$$\text{Impact} = \sigma \cdot k \cdot \left(\frac{Q}{V}\right)^{0.5}$$

Where:
- $\sigma$ = daily volatility
- $k$ = impact coefficient (typically 0.1-0.5)
- $Q$ = trade quantity
- $V$ = average daily volume

```python
def sqrt_market_impact(shares, adv, daily_vol, k=0.3):
    """
    Square-root market impact model.

    Parameters:
        shares: Number of shares to trade
        adv: Average daily volume
        daily_vol: Daily return volatility (e.g., 0.02 for 2%)
        k: Impact coefficient

    Returns:
        Expected impact in basis points
    """
    participation = shares / adv
    impact = daily_vol * k * np.sqrt(participation)
    return impact * 10000  # Convert to bps
```

---

## Cost Estimation for Backtesting

```python
def estimate_transaction_costs(trade_value, adv_value, daily_vol,
                                spread_bps=5, commission_bps=1):
    """
    Estimate total round-trip transaction costs for backtesting.

    Parameters:
        trade_value: Dollar value of trade
        adv_value: Average daily dollar volume
        daily_vol: Daily return volatility
        spread_bps: Half-spread in basis points
        commission_bps: Commission in basis points

    Returns:
        Total cost in basis points (one way)
    """
    participation = trade_value / adv_value

    # Components
    spread_cost = spread_bps
    impact_cost = daily_vol * 10000 * 0.3 * np.sqrt(participation)
    commission_cost = commission_bps

    total = spread_cost + impact_cost + commission_cost
    return {
        'spread': spread_cost,
        'impact': impact_cost,
        'commission': commission_cost,
        'total_bps': total,
        'total_dollars': trade_value * total / 10000
    }
```

---

## Key Insights for Practitioners

1. **Impact is 2-10x larger than spread** for institutional sizes
2. **Square-root law** means splitting a trade in half only reduces impact by 29%, not 50%
3. **Urgency matters:** Patient execution saves money but risks adverse selection
4. **Measure TCA religiously:** See [[Transaction Cost Analysis]] for post-trade analysis
5. **Cost varies by regime:** Vol spikes increase impact; low-vol environments are cheaper
6. **Realistic costs in backtest:** Use 2-3x estimated costs as buffer — you will underestimate

---

## Related Notes
- [[Transaction Cost Analysis]] — Post-trade cost measurement
- [[Implementation Shortfall]] — Measuring execution quality
- [[VWAP Algorithm]] — Benchmark execution strategy
- [[TWAP Algorithm]] — Time-weighted execution
- [[Market Impact Models]] — Price impact fundamentals
- [[Smart Order Routing]] — Venue selection to minimize costs
- [[Fees Commissions and Slippage]] — Foundational cost concepts
- [[Execution MOC]] — Parent section
- [[Backtesting MOC]] — Using cost models in backtests
