# Feature Selection and Importance

In quantitative finance, we are often "feature rich but signal poor." Including irrelevant or redundant features in a model increases the risk of **Overfitting** and degrades the Signal-to-Noise Ratio (SNR). Feature selection is the process of identifying the subset of variables that contain genuine predictive power.

---

## 1. Feature Importance Types

### A. Mean Decrease Impurity (MDI)
Used in Tree-based models (Random Forest, XGBoost). It measures how much each feature reduces the variance (impurity) of the target.
- **Warning:** MDI is biased towards high-cardinality features (e.g., timestamps or unique IDs) and can be misleading in the presence of multicollinearity.

### B. Mean Decrease Accuracy (MDA) / Permutation Importance
Measures the drop in model performance when a specific feature is randomly shuffled.
- **Why:** If the model's accuracy doesn't drop when a feature is scrambled, that feature isn't contributing unique signal.

### C. SHAP Values (SHapley Additive exPlanations)
Based on game theory, SHAP provides a consistent way to attribute the model's output to each feature for every individual sample. It handles non-linear interactions much better than MDI.

---

## 2. Dealing with Multicollinearity

Financial features are highly correlated (e.g., 5-day SMA and 10-day SMA). This "confuses" many ML models.

- **Cluster-based Feature Selection:** Group correlated features using hierarchical clustering and select the "representative" feature from each cluster.
- **Principal Component Analysis (PCA):** Transform correlated features into a smaller set of orthogonal (uncorrelated) components.
- **Correlation Thresholding:** Removing features that have a correlation $> 0.90$ with another feature already in the model.

---

## 3. Advanced Selection Methods

### A. Single Feature Importance (SFI)
Training a separate model for every single feature and measuring its OOS performance. This avoids the "masking effect" where a strong feature makes a weak but useful feature look irrelevant.

### B. Recursive Feature Elimination (RFE)
Iteratively training the model and removing the least important feature until the optimal subset is reached.

### C. LASSO Regression (L1 Regularization)
A linear model that shrinks the coefficients of irrelevant features to exactly zero, performing automatic feature selection.

---

## 4. The Structural vs. Statistical Check

Before accepting a feature, a JPM quant asks:
1.  **Statistical:** Does it pass a t-test? Is the SHAP value significant?
2.  **Structural:** Is there an economic reason for this feature to work? (e.g., "This feature measures the liquidity premium").
3.  **Stability:** Does the feature's importance remain consistent across different market regimes?

---

## 5. Python: Feature Importance with LightGBM

```python
import pandas as pd
import lightgbm as lgb
import matplotlib.pyplot as plt

def plot_importance(X, y):
    # Fit model
    model = lgb.LGBMRegressor(importance_type='gain')
    model.fit(X, y)
    
    # Extract importance
    importance = pd.Series(model.feature_importances_, index=X.columns)
    importance = importance.sort_values(ascending=False)
    
    importance.plot(kind='barh', title='Feature Importance (Gain)')
    plt.show()
    return importance
```

---

## Related Notes
- [[Feature Engineering for Trading]] — Where features are created.
- [[Overfitting]] — Why we need feature selection.
- [[Machine Learning Strategies]] — Implementing these signals.
- [[Linear Algebra in Finance]] — PCA and Multicollinearity.
- [[Model Validation in Finance]] — Testing the final model.
