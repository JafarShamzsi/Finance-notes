# Supervised Learning

Supervised learning trains models on labeled data to predict outcomes. In quant finance, this means predicting returns, direction, volatility, or other target variables from features. It's the most widely used ML paradigm in production trading systems.

---

## Problem Formulation for Finance

### Regression (Continuous Target)
- Predict **next-period return** $r_{t+1}$
- Predict **volatility** $\sigma_{t+1}$
- Predict **spread** movements for [[Pairs Trading]]

### Classification (Categorical Target)
- Predict **direction** (up/down/flat)
- Predict **regime** (trending/mean-reverting) — see [[Regime Detection]]
- Predict **default** probability (credit risk)

### Target Engineering
The target variable matters more than the model:

| Target | Definition | Use Case |
|--------|-----------|----------|
| Simple return | $r_{t+1} = (P_{t+1} - P_t) / P_t$ | Basic prediction |
| Log return | $\ln(P_{t+1}/P_t)$ | Additive across time |
| Risk-adjusted return | $r_{t+1} / \sigma_t$ | Vol-normalized |
| Triple barrier label | First barrier hit: TP, SL, or time | Lopez de Prado method |
| Quantile label | Top/bottom quintile of cross-section | Long/short signal |

### Triple Barrier Labeling (Lopez de Prado)
```python
import numpy as np
import pandas as pd

def triple_barrier_labels(prices, take_profit=0.02, stop_loss=0.02,
                           max_holding=10):
    """
    Label each point based on which barrier is hit first.

    Returns:
        +1: Take-profit hit first (profitable trade)
        -1: Stop-loss hit first (losing trade)
         0: Neither hit within max_holding (timeout)
    """
    labels = pd.Series(0, index=prices.index)

    for i in range(len(prices) - max_holding):
        entry = prices.iloc[i]
        future = prices.iloc[i+1:i+max_holding+1]

        # Check barriers
        tp_hit = future >= entry * (1 + take_profit)
        sl_hit = future <= entry * (1 - stop_loss)

        tp_day = tp_hit.idxmax() if tp_hit.any() else None
        sl_day = sl_hit.idxmax() if sl_hit.any() else None

        if tp_day and sl_day:
            labels.iloc[i] = 1 if tp_day <= sl_day else -1
        elif tp_day:
            labels.iloc[i] = 1
        elif sl_day:
            labels.iloc[i] = -1
        else:
            labels.iloc[i] = 0

    return labels
```

---

## Models for Financial Prediction

### 1. Linear / Ridge / Lasso Regression
```python
from sklearn.linear_model import Ridge, Lasso

def linear_alpha_model(X_train, y_train, X_test, alpha=1.0, model_type='ridge'):
    """
    Regularized linear model for return prediction.
    L2 (Ridge): Shrinks coefficients, keeps all features
    L1 (Lasso): Sparse solution, automatic feature selection
    """
    model = Ridge(alpha=alpha) if model_type == 'ridge' else Lasso(alpha=alpha)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return predictions, model
```

**When to use:** Baseline model, factor models, when interpretability matters.

### 2. Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

def random_forest_signal(X_train, y_train, X_test,
                          n_estimators=500, max_depth=5, min_samples_leaf=50):
    """
    Random Forest for direction prediction.
    Key params:
    - max_depth: Limit to prevent overfitting (5-10 for finance)
    - min_samples_leaf: Large values reduce overfitting
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]  # Probability of class 1
    return proba, model
```

**When to use:** Feature importance analysis, robust to noise, moderate complexity.

### 3. XGBoost / LightGBM (Industry Standard)
```python
import lightgbm as lgb

def lgbm_alpha_model(X_train, y_train, X_test, y_val=None, X_val=None):
    """
    LightGBM — the workhorse of quant ML.
    Fast, handles missing values, excellent performance on tabular data.
    """
    params = {
        'objective': 'regression',
        'metric': 'mae',
        'learning_rate': 0.05,
        'num_leaves': 31,
        'max_depth': 6,
        'min_child_samples': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 0.1,
        'reg_lambda': 1.0,
        'verbose': -1
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    callbacks = [lgb.early_stopping(50)]

    if X_val is not None:
        val_data = lgb.Dataset(X_val, label=y_val)
        model = lgb.train(params, train_data, num_boost_round=1000,
                          valid_sets=[val_data], callbacks=callbacks)
    else:
        model = lgb.train(params, train_data, num_boost_round=500)

    predictions = model.predict(X_test)
    return predictions, model
```

**When to use:** Default choice for any tabular prediction task. Start here.

---

## Feature Importance Methods

### 1. Built-in (Impurity / Gain)
```python
def feature_importance_gain(model, feature_names):
    """LightGBM or XGBoost feature importance by gain."""
    importance = model.feature_importance(importance_type='gain')
    return pd.Series(importance, index=feature_names).sort_values(ascending=False)
```

### 2. Permutation Importance (More Reliable)
```python
from sklearn.inspection import permutation_importance

def permutation_feature_importance(model, X_test, y_test, n_repeats=10):
    """
    Shuffle each feature and measure performance drop.
    More reliable than built-in importance — detects truly useful features.
    """
    result = permutation_importance(model, X_test, y_test,
                                     n_repeats=n_repeats, random_state=42)
    return pd.DataFrame({
        'mean_importance': result.importances_mean,
        'std': result.importances_std
    }, index=X_test.columns).sort_values('mean_importance', ascending=False)
```

### 3. SHAP Values (Best for Interpretation)
```python
import shap

def shap_analysis(model, X_test):
    """
    SHAP values for model interpretation.
    Shows how each feature pushes prediction up/down for each sample.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    # shap.summary_plot(shap_values, X_test)  # Visualization
    return shap_values
```

### Mean Decrease Accuracy (MDA) — Lopez de Prado
```python
def mda_feature_importance(model, X, y, n_splits=5):
    """
    Mean Decrease Accuracy: more robust than permutation importance.
    Uses cross-validated accuracy as the base metric.
    """
    from sklearn.model_selection import cross_val_score
    base_score = cross_val_score(model, X, y, cv=n_splits, scoring='neg_mean_absolute_error').mean()

    importances = {}
    for col in X.columns:
        X_shuffled = X.copy()
        X_shuffled[col] = np.random.permutation(X_shuffled[col].values)
        shuffled_score = cross_val_score(model, X_shuffled, y, cv=n_splits,
                                          scoring='neg_mean_absolute_error').mean()
        importances[col] = base_score - shuffled_score

    return pd.Series(importances).sort_values(ascending=False)
```

---

## Cross-Validation for Finance

**Standard k-fold CV is WRONG for time series** — it looks ahead in time.

### Purged Walk-Forward CV
```python
def purged_kfold_cv(X, y, model, n_splits=5, embargo_pct=0.01):
    """
    Purged k-fold cross-validation for financial data.

    1. Split into k chronological folds
    2. Purge: Remove training samples that overlap with test labels
    3. Embargo: Add gap between train and test to prevent leakage
    """
    n = len(X)
    embargo = int(n * embargo_pct)
    fold_size = n // n_splits
    scores = []

    for i in range(n_splits):
        test_start = i * fold_size
        test_end = min((i + 1) * fold_size, n)

        # Training set: everything except test + embargo
        train_mask = np.ones(n, dtype=bool)
        purge_start = max(0, test_start - embargo)
        purge_end = min(n, test_end + embargo)
        train_mask[purge_start:purge_end] = False

        X_train = X.iloc[train_mask]
        y_train = y.iloc[train_mask]
        X_test = X.iloc[test_start:test_end]
        y_test = y.iloc[test_start:test_end]

        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        scores.append(score)

    return np.array(scores)
```

### Combinatorial Purged CV (CPCV) — Lopez de Prado
Most rigorous method — generates all possible train/test combinations while respecting time ordering.

---

## Ensemble Methods

### Signal Blending
```python
def ensemble_signals(models, X_test, weights=None):
    """
    Combine multiple model predictions.
    Ensemble typically outperforms any single model by 10-20%.
    """
    predictions = [m.predict(X_test) for m in models]

    if weights is None:
        weights = np.ones(len(models)) / len(models)

    blended = sum(w * p for w, p in zip(weights, predictions))
    return blended
```

### Stacking
Train a meta-model on the predictions of base models:
1. Base models predict on validation folds
2. Meta-model (e.g., Ridge) learns optimal combination
3. Reduces overfitting vs simple averaging

---

## Evaluation (Don't Use Accuracy!)

| Metric | Use Case | Formula |
|--------|----------|---------|
| **IC** | Signal quality | $\text{corr}(\hat{r}, r)$ |
| **ICIR** | Signal stability | $\text{mean}(IC) / \text{std}(IC)$ |
| **Sharpe of strategy** | End-to-end | $(R - R_f) / \sigma$ |
| **Hit rate** | Direction prediction | % correct direction |
| **Profit factor** | Risk-adjusted | Gross profit / Gross loss |

See [[Performance Metrics]] and [[Alpha Research]] for more.

---

## Related Notes
- [[ML and AI MOC]] — Parent section
- [[Feature Engineering for Trading]] — Feature construction
- [[Alpha Research]] — Signal pipeline
- [[Overfitting]] — The #1 risk in financial ML
- [[Walk-Forward Analysis]] — Proper validation
- [[Deep Learning]] — Neural network approaches
- [[Unsupervised Learning]] — Clustering and dimensionality reduction
- [[Backtesting MOC]] — Testing ML strategies
- [[Machine Learning Strategies]] — Practical ML trading strategies
