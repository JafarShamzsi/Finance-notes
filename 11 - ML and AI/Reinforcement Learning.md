# Reinforcement Learning

Reinforcement learning (RL) trains agents to make sequential decisions by maximizing cumulative reward through interaction with an environment. In quant finance, the environment is the market, actions are trading decisions, and rewards are risk-adjusted P&L.

---

## RL Framework for Trading

```
                    ┌─────────────────┐
         state s_t  │                 │  reward r_t
    ┌──────────────→│   ENVIRONMENT   │──────────────┐
    │               │   (Market)      │              │
    │               └────────┬────────┘              │
    │                        │ state s_{t+1}         │
    │                        ▼                       ▼
    │               ┌─────────────────┐
    │               │                 │
    └───────────────│     AGENT       │
         action a_t │   (Trading      │
                    │    Algorithm)   │
                    └─────────────────┘
```

### State Space (What the Agent Sees)
| Feature Type | Examples |
|-------------|----------|
| Price data | Returns, volatility, momentum indicators |
| Position data | Current holdings, unrealized P&L, cash |
| Market data | Volume, spread, order book imbalance |
| Technical | RSI, MACD, Bollinger position |
| Portfolio | Correlation, sector exposure, leverage |

### Action Space (What the Agent Can Do)
| Design | Actions | Complexity |
|--------|---------|-----------|
| **Discrete (simple)** | Buy, Hold, Sell | Low |
| **Discrete (sized)** | -100%, -50%, 0%, +50%, +100% | Medium |
| **Continuous** | Target weight $\in [-1, 1]$ | High |

### Reward Function (Critical Design Choice)

| Reward | Formula | Properties |
|--------|---------|-----------|
| Simple return | $r_t = (P_{t+1} - P_t) / P_t \times \text{position}$ | Can ignore risk |
| Risk-adjusted | $r_t - \lambda \cdot r_t^2$ | Penalizes variance |
| Sharpe-like | $\text{mean}(r) / \text{std}(r)$ over window | Promotes consistency |
| Differential Sharpe | $\frac{dSR}{dt}$ incremental | Moody & Saffell (2001) |
| With costs | $r_t - c \cdot |\Delta \text{position}|$ | Realistic |

```python
def differential_sharpe_reward(returns, A_prev=0, B_prev=0, eta=0.01):
    """
    Differential Sharpe Ratio (Moody & Saffell, 2001).
    Incremental update to Sharpe ratio — better for online learning.
    """
    A = A_prev + eta * (returns - A_prev)  # Exponential moving avg of returns
    B = B_prev + eta * (returns**2 - B_prev)  # Exponential moving avg of returns^2

    if B - A**2 > 0:
        dSR = (B * (returns - A) - 0.5 * A * (returns**2 - B)) / (B - A**2)**1.5
    else:
        dSR = 0

    return dSR, A, B
```

---

## Key RL Algorithms for Finance

### 1. Deep Q-Network (DQN) — Discrete Actions

The agent learns Q(s, a) — the expected total reward of taking action $a$ in state $s$.

$$Q(s, a) = r + \gamma \max_{a'} Q(s', a')$$

```python
import numpy as np
import torch
import torch.nn as nn
from collections import deque
import random

class DQNTrader:
    """
    DQN agent for discrete trading actions.
    Actions: 0=Sell, 1=Hold, 2=Buy
    """

    def __init__(self, state_dim, n_actions=3, lr=1e-4,
                 gamma=0.99, epsilon=1.0, epsilon_decay=0.995):
        self.state_dim = state_dim
        self.n_actions = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = 0.01
        self.memory = deque(maxlen=10000)

        # Q-network and target network
        self.q_net = self._build_network()
        self.target_net = self._build_network()
        self.target_net.load_state_dict(self.q_net.state_dict())
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=lr)

    def _build_network(self):
        return nn.Sequential(
            nn.Linear(self.state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, self.n_actions)
        )

    def act(self, state):
        """Epsilon-greedy action selection."""
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        with torch.no_grad():
            q_values = self.q_net(torch.FloatTensor(state))
            return q_values.argmax().item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=64):
        """Experience replay — train on random batch from memory."""
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones)

        # Current Q values
        current_q = self.q_net(states).gather(1, actions.unsqueeze(1))

        # Target Q values
        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0]
            target_q = rewards + (1 - dones) * self.gamma * next_q

        # Update
        loss = nn.MSELoss()(current_q.squeeze(), target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def update_target(self):
        """Copy weights to target network (do every N steps)."""
        self.target_net.load_state_dict(self.q_net.state_dict())
```

### 2. Policy Gradient (REINFORCE) — Continuous Actions

Directly learn a policy $\pi(a|s)$ that maps states to actions.

$$\nabla J(\theta) = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) \cdot R]$$

```python
class PolicyGradientTrader:
    """
    REINFORCE policy gradient for continuous position sizing.
    Output: target portfolio weight in [-1, 1]
    """

    def __init__(self, state_dim, lr=1e-4):
        self.policy = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)  # Mean and log_std
        )
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.log_probs = []
        self.rewards = []

    def act(self, state):
        """Sample action from policy (Gaussian)."""
        state = torch.FloatTensor(state)
        output = self.policy(state)
        mean = torch.tanh(output[0])  # Bound to [-1, 1]
        log_std = output[1].clamp(-2, 0)  # Reasonable std range
        std = torch.exp(log_std)

        dist = torch.distributions.Normal(mean, std)
        action = dist.sample()
        action = action.clamp(-1, 1)  # Enforce bounds

        self.log_probs.append(dist.log_prob(action))
        return action.item()

    def update(self, gamma=0.99):
        """Update policy after episode."""
        # Compute discounted returns
        returns = []
        R = 0
        for r in reversed(self.rewards):
            R = r + gamma * R
            returns.insert(0, R)
        returns = torch.FloatTensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        # Policy gradient loss
        loss = sum(-lp * R for lp, R in zip(self.log_probs, returns))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.log_probs = []
        self.rewards = []
```

### 3. Proximal Policy Optimization (PPO) — State of the Art

PPO clips the policy update to prevent large changes:

$$L^{CLIP}(\theta) = \mathbb{E}\left[\min\left(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]$$

- More stable than vanilla policy gradient
- Industry standard for continuous control
- Use libraries: `stable-baselines3`, `ray[rllib]`

---

## Applications in Finance

### 1. Optimal Execution
**State:** Remaining shares, time left, current spread, volatility
**Action:** How many shares to trade this period
**Reward:** Negative implementation shortfall

Benchmark: [[Transaction Cost Models|Almgren-Chriss]] (analytical), RL can discover nonlinear strategies.

### 2. Portfolio Optimization
**State:** Asset returns, covariance, current weights, transaction costs
**Action:** Target weights for each asset
**Reward:** Risk-adjusted return (Sharpe, Sortino)

See [[Portfolio Optimization]] and [[Portfolio Rebalancing]].

### 3. Market Making
**State:** [[Order Book Dynamics|Order book]], inventory, spread, volatility
**Action:** Bid/ask quote prices and sizes
**Reward:** Spread earned minus inventory risk

See [[Market Making Strategies]].

### 4. Hedging
**State:** Option Greeks, underlying price, time to expiry
**Action:** Hedge ratio (shares of underlying)
**Reward:** Negative hedging error minus transaction costs

Better than [[Greeks Deep Dive|delta-hedging]] when costs and discrete hedging matter.

---

## Challenges and Pitfalls

| Challenge | Problem | Mitigation |
|-----------|---------|-----------|
| **Non-stationarity** | Market regimes change | Rolling retraining, [[Regime Detection]] |
| **Sparse rewards** | Trading returns are noisy | Dense reward shaping, risk-adjusted rewards |
| **Overfitting** | Agent memorizes training data | Regularization, out-of-sample testing |
| **Sim-to-real gap** | Backtest ≠ live market | Realistic simulator with [[Transaction Cost Models|costs]], slippage |
| **Sample efficiency** | Needs millions of episodes | Offline RL, experience replay, transfer learning |
| **Exploration** | Random actions lose money | Warm-start from rule-based policy |

### Practical Tips
1. **Start with a simple baseline** — Rule-based strategy first, then try to beat it with RL
2. **Reward shaping is everything** — Bad reward = bad agent
3. **Use realistic simulators** — Include costs, market impact, latency
4. **Train on multiple regimes** — Bull, bear, sideways, crisis
5. **Validate rigorously** — Walk-forward, [[Walk-Forward Analysis|out-of-sample]]

---

## Related Notes
- [[ML and AI MOC]] — Parent section
- [[Deep Learning]] — Neural network architectures for RL
- [[Supervised Learning]] — Comparison paradigm
- [[Machine Learning Strategies]] — ML-based trading strategies
- [[Transaction Cost Models]] — Execution optimization with RL
- [[Portfolio Optimization]] — RL for portfolio management
- [[Market Making Strategies]] — RL market making
- [[Backtesting MOC]] — Testing RL strategies
