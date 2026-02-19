# Feature Engineering for Trading

Feature engineering is the process of transforming raw market data into predictive signals (alphas). In quantitative finance, the quality of your features (signal-to-noise ratio) often matters more than the complexity of the machine learning model.

---

## 1. Technical Indicators (Momentum & Mean Reversion)

Standard features derived from Price and Volume (OHLCV).

| Category | Features | Calculation / Intuition |
|----------|----------|-------------------------|
| **Trend** | SMA, EMA, MACD | Direction of the move over different windows. |
| **Momentum** | RSI, ROC, MFI | Strength/Velocity of the price change. |
| **Volatility** | ATR, Bollinger Bands | Normalizing returns by the current risk regime. |
| **Volume** | OBV, VWAP, Volume Spikes | Confirming price moves with liquidity. |

```python
import pandas as pd
import pandas_ta as ta

def add_technical_features(df):
    # RSI: Relative Strength Index
    df['RSI'] = ta.rsi(df['close'], length=14)
    
    # ATR: Average True Range (Volatility)
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    
    # MACD
    macd = ta.macd(df['close'])
    df = pd.concat([df, macd], axis=1)
    
    return df
```

---

## 2. Microstructure Features

Derived from L2/L3 order book data and trade flows. See [[Order Book Dynamics]].

- **Order Book Imbalance (OBI):** $(V_{bid} - V_{ask}) / (V_{bid} + V_{ask})$.
- **Micro-Price:** Weighted average of bid/ask by volume.
- **Spread:** Absolute and relative (percentage) spread.
- **Trade Flow Toxicity (VPIN):** Volume-synchronized probability of informed trading.
- **Effective Spread:** $2 \times |P_{trade} - P_{mid}|$.

---

## 3. Statistical Transformations

Financial data is non-stationary and noisy. Transformations are required to make features usable for ML.

- **Log Returns:** $\ln(P_t / P_{t-1})$ (additive over time).
- **Volatility Scaling:** $z_t = r_t / \sigma_t$ (Standardizing features by rolling volatility).
- **Fractional Differentiation:** Preserving memory in time series while achieving stationarity (Lopez de Prado).
- **Quantile Transformation:** Mapping features to a uniform or normal distribution to handle outliers.

---

## 4. Fundamental & Alternative Features

- **Valuation Ratios:** P/E, P/B, EV/EBITDA.
- **Earnings Surprise:** Difference between actual and consensus.
- **Sentiment Scores:** Derived from News and Twitter (see [[Natural Language Processing (NLP)]]).
- **Satellite/Credit Card Data:** Proxy for retail sales or supply chain health.

---

## 5. Cross-Asset & Correlation Features

- **Beta to Market:** Rolling regression coefficient against S&P 500.
- **Pair Spreads:** $P_{Asset A} - \beta \cdot P_{Asset B}$ (see [[Pairs Trading]]).
- **Sector Relative Returns:** Outperformance of a stock relative to its industry peers.
- **Currency Impact:** How the local currency strength affects the stock (e.g., Export-heavy stocks vs. JPY).

---

## 6. Target Labeling (The "Target" is a Feature)

Standard "Next Return" targets are often too noisy.

- **Triple Barrier Labeling:** Fixed TP, SL, and Time-limit (see [[Supervised Learning]]).
- **Trend Scanning:** Labeling periods based on local t-statistics of the trend.
- **Meta-Labeling:** Training a secondary model to predict the *probability* of a primary signal being correct.

---

## Related Notes
- [[Data Engineering MOC]] — Ingestion and storage
- [[Order Book Dynamics]] — Source of microstructure features
- [[Supervised Learning]] — Using features in models
- [[Natural Language Processing (NLP)]] — Unstructured data features
- [[Statistical Arbitrage]] — Multi-asset features
- [[Machine Learning Strategies]] — Putting it all together
