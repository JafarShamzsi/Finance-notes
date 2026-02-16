# Machine Learning and Artificial Intelligence Map of Content

> ML in finance is not about building the most complex model. It's about avoiding overfitting while extracting genuine signal from noisy financial data.

---

## The ML Pipeline for Trading

```
Raw Data → Feature Engineering → Train/Val/Test Split → Model Selection → Hyperparameter Tuning
                                        ↓                                        ↓
                                  Walk-Forward         ←    Cross-Validation (purged)
                                  Validation                        ↓
                                        ↓                   Model Ensemble
                                  Signal Generation              ↓
                                        ↓                   Risk Controls
                                  Portfolio Construction         ↓
                                        ↓                   Live Monitoring
                                  Execution
```

---

## Learning Paradigms
- [[Supervised Learning]] — Predict target variable (returns, direction, volatility)
- [[Unsupervised Learning]] — Find structure (clustering, dimensionality reduction)
- [[Reinforcement Learning]] — Learn optimal trading policy through interaction
- [[Deep Learning]] — Neural networks for complex pattern recognition
- [[Natural Language Processing (NLP)]] — Extract signals from text (news, filings, social media)

---

## ML Models Ranked for Finance

| Model | Interpretability | Overfitting Risk | Best Use Case |
|-------|-----------------|-----------------|---------------|
| **Linear/Logistic** | High | Low | Baseline, factor models |
| **Random Forest** | Medium | Medium | Feature importance, robust signals |
| **XGBoost/LightGBM** | Medium | Medium-High | Best general-purpose for tabular data |
| **LSTM/GRU** | Low | High | Sequential patterns, time series |
| **Transformer** | Low | Very High | NLP, large-scale time series |
| **Autoencoders** | Low | Medium | Anomaly detection, feature extraction |
| **Reinforcement Learning** | Low | Very High | Portfolio optimization, execution |

---

## Critical Pitfalls in Financial ML

### 1. Overfitting (The #1 Problem)
Financial data has very low signal-to-noise ratio (SNR ~0.05 for daily returns). Most "patterns" are noise.

**Prevention:**
- Purged cross-validation (no data leakage between folds)
- Walk-forward analysis (never look ahead)
- Embargo periods between train and test
- Feature importance analysis (drop irrelevant features)
- Regularization (L1, L2, dropout, early stopping)

### 2. Non-Stationarity
Financial relationships change over time. A model trained on 2015-2019 data may fail in 2020.

**Prevention:**
- Rolling retraining (retrain monthly or quarterly)
- Regime detection ([[Regime Detection]])
- Feature engineering that captures relative values, not absolute

### 3. Target Leakage
Using information in features that wouldn't be available at prediction time.

**Prevention:**
- Triple barrier labeling (López de Prado)
- Strict point-in-time data alignment
- No future data in features

### 4. Survivorship Bias
Training on stocks that survived to the present.

**Prevention:**
- Use point-in-time datasets
- Include delisted stocks
- See [[Survivorship Bias]]

---

## Feature Engineering for ML

See [[Feature Engineering for Trading]] for details.

**Categories:**
| Type | Examples |
|------|---------|
| Price-based | Returns, log returns, volatility, skew, kurtosis |
| Volume-based | Volume ratio, dollar volume, volume trend |
| Technical | RSI, MACD, Bollinger position, ATR |
| Cross-sectional | Sector-relative returns, percentile rank |
| Fundamental | P/E, P/B, ROE, earnings surprise |
| Alternative | Sentiment score, satellite data, web traffic |

---

## Model Evaluation

**Never use accuracy for financial ML.** Use:
- **Sharpe Ratio of strategy** — Does the signal make money?
- **Information Coefficient (IC)** — Correlation between predicted and actual returns
- **IC Information Ratio** — Mean IC / Std IC
- **Turnover-adjusted returns** — After transaction costs

---

## Key Resources
- López de Prado — *Advances in Financial ML* (the bible)
- Gu, Kelly, Xiu (2020) — *Empirical Asset Pricing via ML*
- See [[Essential Books]] and [[Key Papers]]

---

## Related Areas
- [[Strategies MOC]] — ML-based strategy implementations
- [[Machine Learning Strategies]] — Practical ML strategy guide
- [[Feature Engineering for Trading]] — Input preparation
- [[Data Engineering MOC]] — Data pipelines for ML
- [[Mathematics MOC]] — Mathematical foundations
- [[Backtesting MOC]] — Validating ML strategies
