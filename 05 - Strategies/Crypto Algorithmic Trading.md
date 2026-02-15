# Crypto Algorithmic Trading

**Core Idea:** Cryptocurrency markets offer unique algorithmic opportunities due to 24/7 trading, fragmented liquidity, high volatility, and less sophisticated competition.

---

## Why Crypto is Different

| Property | Traditional Markets | Crypto Markets |
|---|---|---|
| Hours | Limited | 24/7/365 |
| Regulation | Heavy | Light/evolving |
| Competition | Very sophisticated | Mixed |
| Volatility | 10-20% annual | 60-100%+ annual |
| Fragmentation | Consolidated | Highly fragmented |
| Settlement | T+1/T+2 | Minutes (on-chain) |
| Custody | Brokers/custodians | Self-custody possible |

## Crypto-Specific Strategies

### 1. Cross-Exchange Arbitrage
```python
def cross_exchange_arb(prices_dict, min_spread_bps=20):
    """
    Find arbitrage between exchanges.
    prices_dict: {'binance': 50100, 'coinbase': 50150, 'kraken': 50080}
    """
    exchanges = list(prices_dict.keys())
    opportunities = []

    for buy_ex in exchanges:
        for sell_ex in exchanges:
            if buy_ex == sell_ex:
                continue
            spread = (prices_dict[sell_ex] - prices_dict[buy_ex]) / prices_dict[buy_ex]
            if spread * 10000 > min_spread_bps:
                opportunities.append({
                    'buy': buy_ex,
                    'sell': sell_ex,
                    'spread_bps': spread * 10000,
                    'buy_price': prices_dict[buy_ex],
                    'sell_price': prices_dict[sell_ex]
                })
    return opportunities
```

**Challenges:** Transfer times, withdrawal fees, exchange risk.

### 2. Funding Rate Arbitrage
Perpetual futures have a funding rate mechanism:
```
If funding rate > 0: Longs pay shorts (bullish market)
If funding rate < 0: Shorts pay longs (bearish market)

Strategy:
  When funding rate is high positive:
    Long SPOT + Short PERP = Collect funding (delta neutral)

  Annualized yield: funding_rate × 3 × 365 (8-hour intervals)
  Can yield 20-60% APY in bull markets
```

### 3. DEX/CEX Arbitrage
Price differences between decentralized (Uniswap, etc.) and centralized exchanges.
- AMM pricing: `x * y = k` creates predictable price curves
- MEV (Maximal Extractable Value) — on-chain arbitrage

### 4. Liquidation Cascades
```
Large leveraged positions → price move → liquidation → more price move

Monitor open interest and funding rates for cascade risk
Trade the recovery after cascade flushes
```

### 5. On-Chain Analytics
```python
# Whale wallet monitoring
def whale_alert(transfers, threshold_usd=10_000_000):
    """Large transfers to exchanges often signal selling pressure."""
    large_transfers = transfers[transfers['usd_value'] > threshold_usd]
    to_exchange = large_transfers[large_transfers['to_type'] == 'exchange']
    return to_exchange  # Bearish signal
```

## API Integration

```python
import ccxt  # Universal crypto exchange library

# Connect to multiple exchanges
binance = ccxt.binance({'apiKey': '...', 'secret': '...'})
coinbase = ccxt.coinbase({'apiKey': '...', 'secret': '...'})

# Fetch order books
ob = binance.fetch_order_book('BTC/USDT')
best_bid = ob['bids'][0][0]
best_ask = ob['asks'][0][0]

# Place orders
order = binance.create_limit_buy_order('BTC/USDT', 0.01, 50000)
```

## Risk Considerations

- **Exchange risk** — Exchanges can get hacked, freeze withdrawals (FTX)
- **Regulatory risk** — Rules changing rapidly
- **Smart contract risk** — DeFi protocols can have bugs
- **Liquidity risk** — Can evaporate in seconds during crashes
- **Custody** — Secure key management is critical

---

**Related:** [[Asset Classes]] | [[Strategies MOC]] | [[Trend Following]] | [[Statistical Arbitrage]] | [[API Integration (Brokers)]]
