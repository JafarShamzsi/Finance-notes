# Bid-Ask Spread

The bid-ask spread is the most fundamental cost in trading. It is the price of immediacy — what you pay to transact right now.

---

## Definition

```
Spread = Best Ask - Best Bid
Relative Spread = Spread / Mid Price × 10000 (in basis points)
Half-Spread = Spread / 2 (cost per side)
```

## Components

```
Spread = Adverse Selection + Inventory Risk + Order Processing

1. Adverse Selection: Compensation for trading against informed traders
2. Inventory Risk: Risk of holding unwanted positions
3. Order Processing: Fixed costs of providing quotes
```

## What Affects Spread?

| Factor | Effect on Spread |
|---|---|
| Higher volume | Tighter (more competition) |
| Higher volatility | Wider (more risk) |
| More market makers | Tighter |
| News events | Wider (uncertainty) |
| Larger tick size | Can be wider (minimum spread) |
| Dark pools | Can drain lit book liquidity → wider |

## Measuring Spread

```python
def effective_spread(trade_price, mid_price, side):
    """
    What traders actually pay (accounts for price improvement).
    """
    if side == 'buy':
        return 2 * (trade_price - mid_price)
    else:
        return 2 * (mid_price - trade_price)

def realized_spread(trade_price, mid_price_future, side, delay_seconds=5):
    """
    Market maker's actual profit after price moves.
    Realized spread < Quoted spread due to adverse selection.
    """
    if side == 'buy':
        return 2 * (trade_price - mid_price_future)
    else:
        return 2 * (mid_price_future - trade_price)
```

## Typical Spreads

| Instrument | Spread (bps) |
|---|---|
| AAPL | 1-2 bps |
| SPY ETF | <1 bp |
| Small-cap stock | 10-50 bps |
| EUR/USD | 0.5-1 bp |
| BTC/USD (major exchange) | 1-5 bps |
| Corporate bond | 50-200 bps |

---

**Related:** [[Order Book Dynamics]] | [[Market Making Strategies]] | [[Fees Commissions and Slippage]] | [[Liquidity]] | [[Transaction Cost Analysis]]
