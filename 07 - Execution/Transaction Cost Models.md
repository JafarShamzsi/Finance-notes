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

### Derivation of the Almgren-Chriss Optimal Trajectory

The core of the Almgren-Chriss model is solving an optimization problem to find the trading trajectory that minimizes a combination of expected costs and the variance (risk) of those costs. The problem is formulated as:
$$\text{minimize} \quad E[\text{cost}] + \lambda \cdot \text{Var}[\text{cost}]$$
This is a classic problem in the calculus of variations. We are looking for a function, the trading rate $v(t)$, that minimizes the objective functional.

In discrete time, the objective function is:
$$L(n_1, ..., n_N) = \left( \frac{\eta}{2\tau} \sum_{k=1}^{N} n_k^2 \right) + \left( \lambda \sigma^2 \tau \sum_{k=0}^{N-1} x_k^2 \right)$$
(Ignoring the constant spread and permanent impact terms for the optimization of the trajectory shape).

We need to minimize this subject to the constraint $\sum n_k = X$. This can be solved by setting up a Lagrangian. However, it's more elegant to solve in continuous time and then discretize.

In the continuous-time limit, as $N \to \infty$ and $\tau \to 0$:
- The trading list $\{n_k\}$ becomes a continuous trading rate function $v(t)$.
- The holdings list $\{x_k\}$ becomes a continuous holdings function $x(t) = X - \int_0^t v(s)ds$.
- The summations become integrals.

The objective functional becomes:
$$L[v(t)] = \int_0^T \left( \eta v(t)^2 + \lambda\sigma^2 x(t)^2 \right) dt$$
We want to find the path $x(t)$ that minimizes this functional, subject to the boundary conditions $x(0) = X$ and $x(T) = 0$.

This is a standard problem for the **Euler-Lagrange equation**. The integrand is $L(t, x, \dot{x}) = \eta \dot{x}^2 + \lambda\sigma^2 x^2$, where $\dot{x} = -v(t)$. The Euler-Lagrange equation is:
$$\frac{\partial L}{\partial x} - \frac{d}{dt}\frac{\partial L}{\partial \dot{x}} = 0$$
Let's compute the partial derivatives:
- $\frac{\partial L}{\partial x} = 2 \lambda \sigma^2 x(t)$
- $\frac{\partial L}{\partial \dot{x}} = 2 \eta \dot{x}(t)$
- $\frac{d}{dt}\frac{\partial L}{\partial \dot{x}} = 2 \eta \ddot{x}(t)$

Plugging these into the Euler-Lagrange equation:
$$2 \lambda \sigma^2 x(t) - 2 \eta \ddot{x}(t) = 0$$
$$\ddot{x}(t) - \frac{\lambda \sigma^2}{\eta} x(t) = 0$$
This is a second-order ordinary differential equation. If we define $\kappa^2 = \frac{\lambda \sigma^2}{\eta}$, the equation is $\ddot{x}(t) - \kappa^2 x(t) = 0$.

The general solution to this ODE is of the form:
$$x(t) = A e^{\kappa t} + B e^{-\kappa t}$$
This can be written more conveniently using hyperbolic functions:
$$x(t) = C_1 \cosh(\kappa t) + C_2 \sinh(\kappa t)$$
We now use our boundary conditions to solve for the constants $C_1$ and $C_2$:
1.  **At t=0:** $x(0) = X$.
    $X = C_1 \cosh(0) + C_2 \sinh(0) = C_1 \cdot 1 + C_2 \cdot 0 \implies C_1 = X$.
2.  **At t=T:** $x(T) = 0$.
    $0 = X \cosh(\kappa T) + C_2 \sinh(\kappa T) \implies C_2 = -X \frac{\cosh(\kappa T)}{\sinh(\kappa T)}$.

Substituting the constants back into the general solution:
$$x(t) = X \cosh(\kappa t) - X \frac{\cosh(\kappa T)}{\sinh(\kappa T)} \sinh(\kappa t)$$
$$x(t) = X \frac{\sinh(\kappa T)\cosh(\kappa t) - \cosh(\kappa T)\sinh(\kappa t)}{\sinh(\kappa T)}$$
Using the hyperbolic identity $\sinh(a-b) = \sinh(a)\cosh(b) - \cosh(a)\sinh(b)$, we get the final elegant solution for the optimal holdings trajectory:
$$x(t) = X \cdot \frac{\sinh(\kappa(T - t))}{\sinh(\kappa T)}$$
Discretizing this by setting $t_k = k \cdot \tau$ gives the formula in the code. This trajectory, known as the "sigh" profile, starts trading faster at the beginning and slows down as the position is liquidated, balancing the trade-off between impact and timing risk.

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

### Estimating Model Parameters

The Almgren-Chriss model is powerful, but its parameters must be estimated from real market data. This is typically done by the quant execution team using a large dataset of the firm's own trades.

**Data Required:**
- **Execution data:** A list of your own child orders, including size, price, timestamp, and venue.
- **Market data:** High-frequency snapshots of the order book (L1 or L2) for the traded assets.

**Estimating $\epsilon$ (Half-Spread):**
This is the most straightforward. For each trade, measure the prevailing bid-ask spread at the time of execution. The average half-spread across all trades is a good estimate for $\epsilon$.

**Estimating $\eta$ (Temporary Impact) and $\gamma$ (Permanent Impact):**
This is more complex and requires a regression-based approach on a large sample of "meta-orders" (a parent order sliced into many child orders). For each child order `i` within a parent order `j`:
1.  **Calculate the execution price deviation:** $\Delta P_i = P_i^{\text{exec}} - P_i^{\text{mid}}$ (Execution price vs. arrival mid-price).
2.  **Model this deviation:** The core idea is to model the price change as a function of our trading and other factors. A common regression model is:
    $$\Delta P_i = \eta \cdot v_i + \gamma \cdot \sum_{k=1}^{i-1} v_k + \beta \cdot (\text{market return}) + \alpha$$
    - $v_i$ is the trading rate of the child order (shares/sec). The coefficient on this term, $\eta$, is the temporary impact parameter.
    - $\sum v_k$ is the total volume traded so far in the parent order. Its coefficient, $\gamma$, captures the permanent impact.
    - `market return` is the contemporaneous return of the broader market (e.g., SPY) to control for general market movements.
3.  **Run the regression:** Run a multivariate linear regression of $\Delta P_i$ on these variables across thousands of trades to get statistically significant estimates for $\eta$ and $\gamma$.

**Estimating $\sigma$ (Volatility):**
This is the volatility of the asset's price process itself, not the volatility of costs. It can be estimated using a standard [[GARCH Models|GARCH(1,1)]] model on the asset's mid-price returns, calculated over the same frequency as the trade execution intervals ($\tau$).

### Visualizing the Efficient Frontier

The `efficient_frontier` method in the class calculates the trade-off between expected cost and cost uncertainty (variance). Plotting this frontier is key to understanding the model and selecting a risk aversion parameter $\lambda$.

```python
import matplotlib.pyplot as plt

def plot_efficient_frontier(model):
    """
    Plots the execution efficient frontier from an AlmgrenChriss model instance.
    """
    costs, variances = model.efficient_frontier()
    stdevs = np.sqrt(variances)
    
    # Also plot the two extremes: TWAP and VWAP-like schedules
    twap_model = AlmgrenChriss(model.X, model.T, model.N, model.sigma,
                               model.eta, model.gamma, model.epsilon, risk_aversion=1e-20) # Approx. TWAP
    vwap_model = AlmgrenChriss(model.X, model.T, model.N, model.sigma,
                               model.eta, model.gamma, model.epsilon, risk_aversion=1e-3) # Approx. VWAP
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.plot(stdevs, costs, marker='o', linestyle='-', color='navy', label='Efficient Frontier')
    ax.scatter([np.sqrt(twap_model.cost_variance())], [twap_model.expected_cost()],
               color='red', s=150, zorder=5, label='TWAP (Low Risk Aversion)')
    ax.scatter([np.sqrt(vwap_model.cost_variance())], [vwap_model.expected_cost()],
               color='green', s=150, zorder=5, label='Aggressive (High Risk Aversion)')

    ax.set_title('Almgren-Chriss Execution Efficient Frontier', fontsize=16)
    ax.set_xlabel('Execution Cost Standard Deviation ($)', fontsize=12)
    ax.set_ylabel('Expected Execution Cost ($)', fontsize=12)
    ax.legend()
    ax.grid(True)
    
    plt.show()

# --- Example Usage ---
# First, create a model instance as before
# model = AlmgrenChriss(...)
# plot_efficient_frontier(model)
```
The plot shows that as you trade more aggressively to reduce your risk (cost variance), you incur higher expected market impact costs. A portfolio manager can use this plot to choose a $\lambda$ that matches their tolerance for risk versus cost. A very risk-averse PM would choose a point on the far left (high cost, low variance), while a cost-sensitive PM would choose a point on the right.

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
