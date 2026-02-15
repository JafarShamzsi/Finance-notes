# Trading Sessions and Hours

Timing matters enormously in algorithmic trading. Volume, volatility, and spread patterns change dramatically throughout the day.

---

## US Equity Sessions

| Session | Time (ET) | Characteristics |
|---|---|---|
| Pre-market | 04:00 - 09:30 | Low volume, wide spreads, earnings reactions |
| **Regular** | **09:30 - 16:00** | **Primary session, highest liquidity** |
| Post-market | 16:00 - 20:00 | Low volume, earnings reactions |

### Intraday Patterns (U-Shape)

```
Volume/Volatility
    ▐█▌                                    ▐█▌
    ▐██▌                                  ▐██▌
    ▐███▌                                ▐███▌
    ▐████▌▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▐████▌
    9:30  10:00  11:00  12:00  1:00  2:00  3:00  4:00
    ←Open                  Lunch          Close→
```

- **First 30 min:** Highest volume, overnight news absorption, gap fills
- **Midday (11:30-14:00):** Lowest volume, tightest ranges ("lunchtime lull")
- **Last hour (15:00-16:00):** Volume surges, institutional rebalancing, MOC orders
- **Last 15 min:** Extremely high volume — closing auction

### Algo Implications
- [[Mean Reversion Strategies]] work better at open (overreactions)
- [[Momentum Strategies]] often fire mid-morning (10:00-11:00)
- Execution algos ([[VWAP Algorithm]]) must model this U-shape
- Avoid trading during lunch (high spread, low fill rates)

## Global Sessions

| Market | Local Time | ET Equivalent |
|---|---|---|
| Tokyo (TSE) | 09:00-15:00 JST | 19:00-01:00 ET |
| London (LSE) | 08:00-16:30 GMT | 03:00-11:30 ET |
| New York (NYSE) | 09:30-16:00 ET | — |
| Sydney (ASX) | 10:00-16:00 AEST | 18:00-00:00 ET |

### Session Overlaps
- **London-NY overlap (08:00-11:30 ET):** Highest FX volume globally
- **Tokyo-London overlap:** Limited but important for Asian-European flow

## Key Dates and Events

| Event | Impact | Strategy |
|---|---|---|
| **FOMC Meetings** (8x/year) | Massive volatility | Reduce size or trade the reaction |
| **NFP / Jobs Report** (monthly, 1st Fri) | FX, bonds, equities spike | News-based strategies |
| **Earnings Season** (quarterly) | Individual stock vol spikes | Event-driven strategies |
| **Options Expiration** (monthly/weekly Fri) | Pin risk, gamma exposure | Adjust positions |
| **Index Rebalancing** (quarterly) | Forced buying/selling known stocks | Front-run/provide liquidity |
| **Holidays** | Low volume, erratic behavior | Reduce or pause trading |

## Crypto Markets
- **24/7/365** — no sessions, no holidays
- Weekend volatility can be extreme with thin liquidity
- Asian session tends to set trends, US session amplifies

---

**Related:** [[Financial Markets Overview]] | [[VWAP Algorithm]] | [[Liquidity]] | [[Bid-Ask Spread]]
