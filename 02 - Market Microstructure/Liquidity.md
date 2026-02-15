# Liquidity

The ability to buy or sell an asset quickly, at a fair price, without significantly moving the market. The lifeblood of all trading strategies.

---

## Dimensions of Liquidity

| Dimension | Definition | Measure |
|---|---|---|
| **Tightness** | Cost of a round-trip trade | [[Bid-Ask Spread]] |
| **Depth** | Volume available at current prices | Order book depth |
| **Resilience** | Speed of price recovery after large trade | Time to revert |
| **Breadth** | Volume of orders | Daily traded volume |
| **Immediacy** | Speed of execution | Time to fill |

## Measuring Liquidity

```python
def liquidity_metrics(trades_df, orderbook_snapshots):
    """Comprehensive liquidity measurement."""
    metrics = {}

    # Amihud illiquidity ratio (higher = less liquid)
    metrics['amihud'] = (abs(trades_df['return']) /
                         trades_df['dollar_volume']).mean()

    # Volume
    metrics['adv'] = trades_df['volume'].mean()  # Average daily volume
    metrics['dollar_volume'] = trades_df['dollar_volume'].mean()

    # Turnover
    metrics['turnover'] = trades_df['volume'].sum() / shares_outstanding

    # Spread
    metrics['avg_spread'] = orderbook_snapshots['spread'].mean()

    return metrics
```

## Liquidity Risk

Liquidity disappears when you need it most:
- **Market crashes** — Everyone sells, no buyers
- **News events** — Market makers widen/pull quotes
- **End of day** — Liquidity thins out
- **Small caps** — Structurally illiquid

### Liquidity Crisis Pattern
```
Normal: Tight spreads, deep books, easy execution
         ↓ (shock event)
Stress:  Spreads widen 10x, depth vanishes, fills at terrible prices
         ↓ (further selling)
Crisis:  Market makers withdraw, circuit breakers, flash crash
```

## Impact on Strategy Design

| Strategy Requirement | Liquid Markets | Illiquid Markets |
|---|---|---|
| Position sizing | Larger positions OK | Must limit size |
| Execution | Market orders fine | Limit orders only |
| Slippage | Low | Significant |
| Capacity | High | Limited |
| Alpha available | Less (more competition) | More (fewer participants) |

---

**Related:** [[Market Microstructure MOC]] | [[Bid-Ask Spread]] | [[Market Impact]] | [[Order Book Dynamics]] | [[Fees Commissions and Slippage]]
