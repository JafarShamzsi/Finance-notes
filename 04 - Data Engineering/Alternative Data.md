# Alternative Data

Non-traditional data sources that can provide an informational edge. The frontier of modern alpha generation.

---

## Categories

### Sentiment & Text Data
| Source | Signal | Latency |
|---|---|---|
| News articles | Event-driven sentiment | Seconds |
| Social media (Twitter/X, Reddit) | Retail sentiment, viral momentum | Real-time |
| Earnings call transcripts | Management tone, guidance | Hours |
| SEC filings (8-K, 10-Q) | Material events, financial health | Minutes |
| Patent filings | Innovation pipeline | Days |
| Job postings | Company growth/contraction | Weekly |

See [[Sentiment-Based Strategies]] and [[Natural Language Processing for Finance]].

### Satellite & Geospatial
| Source | Signal |
|---|---|
| Parking lot car counts | Retail foot traffic → revenue |
| Oil tanker tracking (AIS) | Supply/demand for crude |
| Crop health (NDVI) | Agricultural commodity outlook |
| Construction activity | Real estate, industrial |
| Night-time light intensity | Economic activity |

### Transaction & Consumer
| Source | Signal |
|---|---|
| Credit card transactions | Real-time revenue estimates |
| App download/usage data | Tech company growth |
| Web traffic (SimilarWeb) | Company engagement |
| Point of sale data | Product-level sales |
| Email receipt data | E-commerce trends |

### Supply Chain & Industrial
| Source | Signal |
|---|---|
| Shipping/logistics data | Supply chain health |
| Commodity inventory levels | Physical market tightness |
| Weather data | Energy, agriculture impact |
| Government contracts | Revenue visibility |

## Using Alternative Data

```python
# Example: Google Trends as a trading signal
from pytrends.request import TrendReq

def google_trends_signal(keyword, ticker_prices, lookback=30):
    """
    High search interest can predict retail flow.
    """
    pytrends = TrendReq()
    pytrends.build_payload([keyword], timeframe='today 3-m')
    trend_data = pytrends.interest_over_time()

    # Z-score of search interest
    recent = trend_data[keyword]
    z_score = (recent - recent.rolling(lookback).mean()) / recent.rolling(lookback).std()

    # Extreme interest often precedes reversals
    signal = pd.Series(0, index=z_score.index)
    signal[z_score > 2] = -1   # Contrarian: too much attention
    signal[z_score < -1] = 1   # Under the radar
    return signal
```

## Challenges

| Challenge | Mitigation |
|---|---|
| **Short history** | Limit backtest conclusions, focus on economic logic |
| **Expensive** | Start with free sources (EDGAR, Google Trends) |
| **Noisy** | Combine with price-based signals |
| **Decaying alpha** | Alpha degrades as data becomes commoditized |
| **Look-ahead bias** | Use point-in-time data only |
| **Legal/compliance** | Ensure data is legally obtained |

## Alpha Decay of Alt Data

```
Discovery → Early Adopters → Mainstream → Commoditized → No Alpha

Timeline: 6 months → 1-2 years → 3-5 years → After
```

The best alt data strategies use novel combinations or proprietary sources.

---

**Related:** [[Data Engineering MOC]] | [[Sentiment-Based Strategies]] | [[Natural Language Processing for Finance]] | [[Feature Engineering for Trading]]
