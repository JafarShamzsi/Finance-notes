# Event-Driven Strategies

Event-driven strategies exploit predictable price patterns around corporate and market events. These strategies often capture **structural edges** — inefficiencies driven by institutional constraints, behavioral biases, and information asymmetry rather than speed or model complexity.

---

## Event Taxonomy

```
                        EVENT-DRIVEN
                            |
          +-----------------+------------------+
          |                 |                  |
     Corporate Events   Market Events    Macro Events
          |                 |                  |
    +-----------+     +----------+      +---------+
    |     |     |     |    |     |      |    |    |
  Earn  M&A  Corp   Idx  OPEX  FOMC   CPI  NFP  ECB
  ings  Arb  Action Rebal             GDP
```

---

## Earnings Strategies

### Pre-Earnings Drift
Stocks tend to drift in the direction of the upcoming earnings surprise **before** the announcement.

**Edge source:** Analysts are slow to update estimates; insiders and connected traders accumulate early.

### Post-Earnings Announcement Drift (PEAD)
Stocks continue to drift in the direction of the earnings surprise for 60-90 days after.

**Edge source:** Behavioral underreaction — investors anchor on prior estimates.

```python
import numpy as np
import pandas as pd

def earnings_surprise(actual_eps, consensus_eps, price, std_estimate=None):
    """
    Compute standardized earnings surprise (SUE).

    SUE = (Actual - Consensus) / std(Estimate) or / Price
    """
    if std_estimate is not None and std_estimate > 0:
        sue = (actual_eps - consensus_eps) / std_estimate
    else:
        sue = (actual_eps - consensus_eps) / price * 100  # as % of price
    return sue


def pead_strategy(earnings_df, returns_df, holding_days=63, top_pct=0.2):
    """
    Post-Earnings Announcement Drift strategy.

    Parameters:
        earnings_df: DataFrame with ['date', 'ticker', 'sue'] columns
        returns_df: DataFrame of daily returns (dates × tickers)
        holding_days: Days to hold after earnings
        top_pct: Percentile cutoff for long/short

    Returns:
        Strategy returns
    """
    signals = pd.DataFrame(0, index=returns_df.index, columns=returns_df.columns)

    for _, row in earnings_df.iterrows():
        ticker = row['ticker']
        date = row['date']
        sue = row['sue']

        if ticker not in signals.columns:
            continue

        # Find the index position of the earnings date
        idx = signals.index.get_indexer([date], method='ffill')[0]
        if idx < 0:
            continue

        # Set signal for holding period
        end_idx = min(idx + holding_days, len(signals) - 1)
        if sue > 0:
            signals.iloc[idx:end_idx][ticker] = 1  # Long on positive surprise
        else:
            signals.iloc[idx:end_idx][ticker] = -1  # Short on negative surprise

    # Normalize to equal weight
    n_active = signals.abs().sum(axis=1).replace(0, 1)
    weights = signals.div(n_active, axis=0)

    strategy_returns = (weights.shift(1) * returns_df).sum(axis=1)
    return strategy_returns
```

### Earnings Volatility Trading
Earnings announcements cause vol spikes. Strategies:
1. **Straddle before earnings:** Long vol (profit from large move)
2. **Sell vol after earnings:** Harvest vol crush (IV drops post-event)
3. **Calendar spread:** Sell short-dated, buy long-dated (capture term structure)

See [[Volatility Trading]] and [[Options Strategies for Algos]].

---

## Merger Arbitrage (M&A Arb)

### The Setup
When Company A announces acquisition of Company B:
- **Target (B)** stock jumps toward deal price but trades at a **discount** (deal spread)
- **Acquirer (A)** often drops slightly

### The Trade
- **Long target** at discount to deal price
- **Short acquirer** (for stock deals, hedge ratio = exchange ratio)
- **Earn the spread** if deal closes

### Deal Spread
$$\text{Spread} = \frac{\text{Deal Price} - \text{Current Price}}{\text{Current Price}}$$

Annualized: $\text{Annualized Spread} = \text{Spread} \times \frac{365}{\text{Days to Close}}$

### Risk Factors

| Risk | Impact | Mitigation |
|------|--------|------------|
| Deal break | Target drops 20-40% | Diversify across many deals |
| Regulatory block | Spread widens | Analyze antitrust risk |
| Financing failure | Deal collapses | Monitor credit conditions |
| Timeline extension | Lower annualized return | Factor expected delay |
| Hostile / competing bid | Target rises above deal price | Optionality value |

```python
def merger_arb_signal(target_price, deal_price, deal_type='cash',
                       acquirer_price=None, exchange_ratio=None,
                       expected_close_days=90):
    """
    Evaluate merger arb opportunity.

    Parameters:
        target_price: Current target stock price
        deal_price: Announced deal price (cash) or implied price (stock)
        deal_type: 'cash' or 'stock'
        expected_close_days: Expected days to deal close
    """
    if deal_type == 'stock' and exchange_ratio:
        implied_price = acquirer_price * exchange_ratio
        spread = (implied_price - target_price) / target_price
    else:
        spread = (deal_price - target_price) / target_price

    annualized = spread * 365 / expected_close_days

    return {
        'spread': spread,
        'annualized_return': annualized,
        'attractive': annualized > 0.06  # >6% annualized threshold
    }
```

---

## Index Rebalancing

When stocks are added to or removed from major indices (S&P 500, Russell 2000), index funds must buy/sell. This creates predictable demand.

### The Edge
- **Additions:** Buy pressure from index funds → stock rises 2-5% around effective date
- **Deletions:** Sell pressure → stock drops 2-5%
- **Announcement to effective:** Typically 5-7 trading days

### Strategy
1. **Buy additions** on announcement, sell on effective date (or shortly after)
2. **Short deletions** on announcement, cover on effective date
3. Front-run the predictable flow

```python
def index_rebalance_strategy(announcements, returns_df, hold_days=5):
    """
    Index rebalancing strategy.

    Parameters:
        announcements: DataFrame with ['date', 'ticker', 'action']
                       action: 'add' or 'remove'
    """
    signals = pd.DataFrame(0, index=returns_df.index, columns=returns_df.columns)

    for _, row in announcements.iterrows():
        ticker = row['ticker']
        date = row['date']
        action = row['action']

        if ticker not in signals.columns:
            continue

        idx = signals.index.get_indexer([date], method='ffill')[0]
        end_idx = min(idx + hold_days, len(signals) - 1)

        if action == 'add':
            signals.iloc[idx:end_idx][ticker] = 1
        elif action == 'remove':
            signals.iloc[idx:end_idx][ticker] = -1

    n_active = signals.abs().sum(axis=1).replace(0, 1)
    weights = signals.div(n_active, axis=0)
    return (weights.shift(1) * returns_df).sum(axis=1)
```

### Russell Reconstitution (June)
The biggest annual rebalancing event:
- Russell 2000/3000 reconstituted based on market cap
- ~$9 trillion benchmarked to Russell indices
- Predictable additions/deletions based on public market cap data
- Massive volume on reconstitution day

---

## Corporate Actions

### Spin-Offs
Parent company spins off a subsidiary → forced selling by index funds and mandate-restricted investors.
- **Edge:** Spin-offs often undervalued initially (Joel Greenblatt's strategy)
- Hold 6-12 months for mean reversion

### Share Buybacks
- Announced buybacks signal management confidence
- Stocks with active buybacks outperform by ~2% annually
- See [[Alpha Research]] for factor construction

### Dividend Changes
- Dividend initiation → positive signal (2-3% abnormal return)
- Dividend cuts → negative signal (large drop)
- Omission → very negative

---

## FOMC and Macro Events

### Pre-FOMC Drift
Stocks drift up in the 24 hours before FOMC announcements (Lucca & Moench, 2015):
- Most of annual S&P 500 returns occur in pre-FOMC windows
- Exploitable with simple long SPY position day before FOMC

### Event Vol Patterns
| Event | Typical IV Premium | Vol Crush After |
|-------|-------------------|-----------------|
| **Earnings** | 5-15% IV premium | 50-80% crush |
| **FOMC** | 2-5% IV premium | 30-50% crush |
| **CPI/NFP** | 1-3% IV premium | 20-40% crush |
| **Elections** | 5-20% IV premium | 60-90% crush |

---

## Risk Management for Event Strategies

1. **Diversification:** Trade many events, don't concentrate on one
2. **Position sizing:** Size by expected loss if event goes wrong (see [[Position Sizing]])
3. **Correlation awareness:** Many events cluster (e.g., earnings season)
4. **Liquidity:** Events cause liquidity to dry up — use limit orders
5. **Stop losses:** Tight stops for binary events (earnings, deal break)

---

## Related Notes
- [[Strategies MOC]] — Strategy overview
- [[Alpha Research]] — Signal construction from events
- [[Momentum Strategies]] — PEAD overlaps with momentum
- [[Volatility Trading]] — Event vol strategies
- [[Options Strategies for Algos]] — Earnings straddles, vol crush plays
- [[Factor Investing]] — Event-based factors
- [[Market Microstructure MOC]] — Microstructure around events
- [[Backtesting MOC]] — Event study methodology
