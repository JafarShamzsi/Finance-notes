# Machine Learning Strategies

**Core Idea:** Use ML models to discover non-linear patterns in market data that traditional statistical methods miss.

---

## ML Pipeline for Trading

```
Raw Data → Feature Engineering → Train/Val/Test Split → Model Training
    → Hyperparameter Tuning → Walk-Forward Validation → Signal Generation
    → Position Sizing → Execution → Performance Monitoring
```

**CRITICAL:** Financial ML is different from regular ML. See [[Model Validation in Finance]].

## Feature Categories

### Price-Based Features
```python
def price_features(df, windows=[5, 10, 20, 60]):
    features = pd.DataFrame(index=df.index)
    for w in windows:
        features[f'return_{w}d'] = df['close'].pct_change(w)
        features[f'volatility_{w}d'] = df['close'].pct_change().rolling(w).std()
        features[f'skew_{w}d'] = df['close'].pct_change().rolling(w).skew()
        features[f'kurt_{w}d'] = df['close'].pct_change().rolling(w).kurt()
        features[f'max_return_{w}d'] = df['close'].pct_change().rolling(w).max()
        features[f'min_return_{w}d'] = df['close'].pct_change().rolling(w).min()
    return features
```

### Volume-Based Features
```python
def volume_features(df, windows=[5, 10, 20]):
    features = pd.DataFrame(index=df.index)
    for w in windows:
        features[f'volume_ma_ratio_{w}d'] = df['volume'] / df['volume'].rolling(w).mean()
        features[f'dollar_volume_{w}d'] = (df['close'] * df['volume']).rolling(w).mean()
        features[f'volume_trend_{w}d'] = df['volume'].rolling(w).apply(
            lambda x: np.polyfit(range(len(x)), x, 1)[0])
    return features
```

### Technical Features
```python
def technical_features(df):
    features = pd.DataFrame(index=df.index)
    features['rsi_14'] = compute_rsi(df['close'], 14)
    features['macd'] = compute_macd(df['close'])
    features['bb_position'] = compute_bb_position(df['close'])
    features['atr_ratio'] = compute_atr(df, 14) / df['close']
    return features
```

See [[Feature Engineering for Trading]] for comprehensive feature guide.

## Model Approaches

### 1. Random Forest / Gradient Boosting
Best starting point. Handles non-linearity, feature interactions, resistant to overfitting.

```python
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb

def train_xgboost_model(X_train, y_train, X_val, y_val):
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        min_child_weight=10
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    return model
```

### 2. LSTM / Deep Learning
For sequential/temporal patterns. See [[Deep Learning for Time Series]].

```python
import torch
import torch.nn as nn

class LSTMPredictor(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                           batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        return self.sigmoid(self.fc(last_hidden))
```

### 3. Reinforcement Learning
See [[Reinforcement Learning for Trading]].

### 4. Ensemble Methods
Combine multiple models for robust signals:
```python
def ensemble_signal(models, features):
    predictions = [model.predict_proba(features)[:, 1] for model in models]
    return np.mean(predictions, axis=0)
```

## Critical Pitfalls

### 1. Overfitting (The #1 Problem)
```
In-sample Sharpe: 3.0  →  Out-of-sample Sharpe: 0.3
```

**Prevention:**
- [[Walk-Forward Analysis]] — never look ahead
- Embargo period between train and test
- Combinatorial purged cross-validation
- Limit model complexity (regularization)
- [[Feature Selection and Importance]] — fewer features

### 2. Non-Stationarity
Markets change over time. Models trained on 2015 data may not work in 2025.

### 3. Look-Ahead Bias
Any feature computed using future data will inflate performance. See [[Look-Ahead Bias]].

### 4. Target Leakage
Features that contain information about the target variable through indirect channels.

## Walk-Forward Framework

```python
def walk_forward_backtest(data, model_class, train_window=252,
                          test_window=21, retrain_every=21):
    """
    Rolling train/test with embargo.
    """
    results = []

    for start in range(0, len(data) - train_window - test_window, retrain_every):
        train_end = start + train_window
        test_end = train_end + test_window

        # Embargo: skip 5 days between train and test
        embargo = 5
        X_train = data.features[start:train_end - embargo]
        y_train = data.target[start:train_end - embargo]
        X_test = data.features[train_end:test_end]
        y_test = data.target[train_end:test_end]

        model = model_class()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        results.append({
            'period': data.index[train_end:test_end],
            'predictions': predictions,
            'actual': y_test
        })

    return results
```

## Performance Expectations

| Approach | Typical Sharpe | Complexity | Data Needs |
|---|---|---|---|
| Linear models | 0.3-0.8 | Low | Low |
| Tree-based (XGBoost) | 0.5-1.5 | Medium | Medium |
| Deep learning | 0.5-2.0 | High | High |
| Ensemble | 0.8-2.0 | High | High |
| RL | Variable | Very High | Very High |

---

**Related:** [[ML and AI MOC]] | [[Feature Engineering for Trading]] | [[Model Validation in Finance]] | [[Overfitting and Curve Fitting]] | [[Walk-Forward Analysis]]
