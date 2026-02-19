# Unsupervised Learning

Unsupervised learning finds hidden patterns in data without explicit labels. In quant finance, it's used for regime detection, dimensionality reduction, clustering similar assets, and extracting latent factors.

---

## 1. Dimensionality Reduction

High-dimensional financial data (e.g., returns of 500 stocks) is noisy. Dimensionality reduction compresses this into a few "latent drivers."

### Principal Component Analysis (PCA)
PCA finds orthogonal directions (principal components) that explain the most variance in returns.

**Applications:**
- **Eigen-portfolios:** The first PC often represents the "Market" factor. Subsequent PCs represent sectors or styles.
- **De-noising:** Reconstruct the covariance matrix using only the top $k$ components to remove noise.
- **Factor Discovery:** Identifying latent risk factors.

```python
from sklearn.decomposition import PCA
import pandas as pd

def compute_eigen_portfolios(returns, n_components=5):
    """
    Compute PCA-based eigen-portfolios from a return matrix.
    """
    pca = PCA(n_components=n_components)
    pca.fit(returns)

    # Components are the 'loadings' for each portfolio
    components = pd.DataFrame(
        pca.components_.T,
        index=returns.columns,
        columns=[f'PC{i+1}' for i in range(n_components)]
    )

    # Explained variance tells us how much 'risk' each factor captures
    explained_var = pca.explained_variance_ratio_

    return components, explained_var
```

---

## 2. Clustering for Asset Selection

Grouping assets by behavior rather than sector/industry.

### K-Means for Regime Detection
Clustering time-series features (volatility, trend, spread) to identify market states.
- **Regime 1:** Low vol, steady uptrend (Bull)
- **Regime 2:** High vol, no trend (Choppy)
- **Regime 3:** High vol, sharp downtrend (Crash)

### Hierarchical Risk Parity (HRP)
Uses hierarchical clustering on the correlation matrix to build a diversified portfolio tree.
- Unlike Mean-Variance, HRP does not require matrix inversion (more stable).
- See [[Risk Parity]] for implementation.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_market_regimes(features, n_clusters=3):
    """
    Use K-Means to identify latent market regimes.
    Features: Volatility, Returns, RSI, etc.
    """
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    regimes = model.fit_predict(scaled_features)

    return regimes
```

---

## 3. Manifold Learning (Non-linear)

Financial relationships are often non-linear. Linear PCA may miss complex structures.

- **t-SNE / UMAP:** Excellent for visualizing high-dimensional asset clusters in 2D.
- **Autoencoders:** Neural networks that learn a compressed representation (bottleneck) of input data.

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def visualize_asset_clusters(returns):
    """
    Visualize 500 stocks in 2D space based on correlation.
    Stocks that move together will cluster together.
    """
    corr = returns.corr()
    dist = 1 - corr  # Distance metric

    tsne = TSNE(n_components=2, metric='precomputed', init='random')
    embeddings = tsne.fit_transform(dist)

    plt.scatter(embeddings[:, 0], embeddings[:, 1])
    plt.title('Asset Clusters via t-SNE')
    plt.show()
```

---

## 4. Latent Dirichlet Allocation (LDA) for NLP

Unsupervised topic modeling on SEC filings, news, or earnings transcripts.
- Identify "topics" (e.g., Supply Chain, ESG, Inflation) without manual tagging.
- See [[Natural Language Processing (NLP)]] for more.

---

## Summary of Techniques

| Technique | Financial Use Case | Benefit |
|-----------|-------------------|---------|
| **PCA** | Factor modeling, de-noising | Interpretability, risk decomposition |
| **K-Means** | Regime detection | Objective state identification |
| **HRP** | Portfolio optimization | Numerical stability, diversification |
| **Autoencoders** | Feature engineering | Non-linear compression |
| **Isolation Forest** | Anomaly/Fraud detection | Robust to outliers |

---

## Related Notes
- [[ML and AI MOC]] — Master navigation
- [[Regime Detection]] — Deep dive into states
- [[Risk Parity]] — HRP implementation
- [[Factor Models]] — PCA connection
- [[Portfolio Optimization]] — Using clusters for allocation
- [[Mathematics MOC]] — Linear algebra foundations
