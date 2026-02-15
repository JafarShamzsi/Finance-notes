# Sentiment-Based Strategies

**Core Idea:** Extract trading signals from text, social media, news, and other unstructured data sources using NLP and sentiment analysis.

---

## Data Sources

| Source | Latency | Signal Strength | Coverage |
|---|---|---|---|
| **News wires** (Reuters, Bloomberg) | Seconds | High | Broad |
| **Earnings call transcripts** | Hours | Medium | Equities |
| **SEC filings** (10-K, 10-Q, 8-K) | Minutes-Hours | Medium | Equities |
| **Twitter/X** | Real-time | Variable | Broad |
| **Reddit** (r/wallstreetbets) | Real-time | Low-Medium | Meme stocks |
| **StockTwits** | Real-time | Low | Equities |
| **Google Trends** | Daily | Medium | Broad |
| **Analyst reports** | Daily | Medium | Equities |

## Sentiment Scoring

### Dictionary-Based
```python
from textblob import TextBlob

def simple_sentiment(text):
    """TextBlob polarity: -1 (negative) to +1 (positive)."""
    return TextBlob(text).sentiment.polarity
```

### FinBERT (Finance-Specific Transformer)
```python
from transformers import pipeline

finbert = pipeline("sentiment-analysis",
                   model="ProsusAI/finbert")

def finbert_sentiment(text):
    result = finbert(text[:512])[0]
    # Returns: {'label': 'positive/negative/neutral', 'score': 0.0-1.0}
    score = result['score']
    if result['label'] == 'negative':
        score = -score
    elif result['label'] == 'neutral':
        score = 0
    return score
```

### Aggregate Sentiment Signal
```python
def daily_sentiment_signal(articles, ticker):
    """
    Aggregate sentiment from multiple articles.
    """
    scores = []
    for article in articles:
        if ticker in article['tickers']:
            score = finbert_sentiment(article['text'])
            # Weight by recency
            hours_old = (datetime.now() - article['timestamp']).hours
            weight = np.exp(-hours_old / 12)  # Half-life of 12 hours
            scores.append(score * weight)

    if not scores:
        return 0

    return np.mean(scores)
```

## Trading Strategies

### 1. News Momentum
```
Positive news → Buy and hold for 1-5 days
Negative news → Short and hold for 1-5 days

Key insight: Markets underreact to news initially, then drift
```

### 2. Sentiment Reversal
```
Extreme positive sentiment → Contrarian short (overcrowded)
Extreme negative sentiment → Contrarian long (panic selling)
```

### 3. Sentiment + Price Divergence
```
Price falling + Sentiment improving → Buy (divergence, early signal)
Price rising + Sentiment deteriorating → Sell (smart money exiting)
```

### 4. Social Media Volume Anomaly
```python
def social_volume_signal(mentions, lookback=30, threshold=3.0):
    """Unusual social media activity as signal."""
    mean_mentions = mentions.rolling(lookback).mean()
    std_mentions = mentions.rolling(lookback).std()
    z_score = (mentions - mean_mentions) / std_mentions

    # Unusual attention often precedes moves
    return z_score > threshold
```

## Performance Notes

- Sentiment signals decay fast (hours to days)
- Best combined with [[Momentum Strategies]] or [[Mean Reversion Strategies]]
- Beware of regime-dependent performance
- Social media signals prone to manipulation

---

**Related:** [[Natural Language Processing for Finance]] | [[Alternative Data]] | [[Machine Learning Strategies]] | [[Feature Engineering for Trading]]
