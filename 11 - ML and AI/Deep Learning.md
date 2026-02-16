# Deep Learning

Deep learning uses neural networks with multiple hidden layers to learn hierarchical representations of data. In finance, it's most useful for NLP, time-series forecasting, and feature extraction.

---

## Architecture Overview

### Feedforward Neural Networks (FNNs)
Simplest architecture. Input → Hidden layers → Output.

```python
import torch
import torch.nn as nn

class AlphaNet(nn.Module):
    """Simple feedforward net for return prediction."""
    def __init__(self, n_features, hidden_sizes=[128, 64, 32]):
        super().__init__()
        layers = []
        prev_size = n_features
        for h in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, h),
                nn.BatchNorm1d(h),
                nn.ReLU(),
                nn.Dropout(0.3)
            ])
            prev_size = h
        layers.append(nn.Linear(prev_size, 1))  # Predict return
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)
```

**Use in finance:** Cross-sectional return prediction from tabular features. Competes with XGBoost but often loses on tabular data.

---

### Recurrent Neural Networks (RNNs) / LSTM / GRU

Process sequential data. LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit) solve the vanishing gradient problem.

```python
class LSTMPredictor(nn.Module):
    """LSTM for time series prediction."""
    def __init__(self, n_features, hidden_size=64, n_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=n_layers,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x shape: (batch, seq_len, n_features)
        lstm_out, (h_n, c_n) = self.lstm(x)
        # Use last hidden state
        last_hidden = lstm_out[:, -1, :]
        return self.fc(last_hidden)
```

**Use in finance:**
- Price prediction (limited success)
- Volatility forecasting (better success)
- Order flow prediction
- Limit order book modeling

**LSTM vs GRU:** GRU is simpler (2 gates vs 3), trains faster, often similar performance. Default to GRU unless you have a reason for LSTM.

---

### Convolutional Neural Networks (CNNs)

Originally for images, but useful for financial time series when treated as 1D signals or 2D "images" (time × features).

**Use in finance:**
- Chart pattern recognition (candlestick patterns as images)
- Feature extraction from LOB (limit order book) snapshots
- Multi-asset correlation structure detection

---

### Transformers / Attention Mechanisms

The dominant architecture for NLP. Increasingly used for time series.

```python
class TransformerPredictor(nn.Module):
    """Transformer for multi-asset time series."""
    def __init__(self, n_features, d_model=64, nhead=4, n_layers=2):
        super().__init__()
        self.input_proj = nn.Linear(n_features, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead,
            dim_feedforward=d_model * 4, dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, n_layers)
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        # x shape: (batch, seq_len, n_features)
        x = self.input_proj(x)
        x = self.transformer(x)
        x = x[:, -1, :]  # Last time step
        return self.fc(x)
```

**Use in finance:**
- NLP: Earnings calls, SEC filings, news sentiment (FinBERT)
- Multi-asset attention: Which assets inform which?
- Long-range dependencies in time series

---

### Autoencoders

Compress data into a lower-dimensional representation, then reconstruct. The bottleneck learns a compressed representation.

**Use in finance:**
- **Anomaly detection** — Reconstruct normal market conditions; high reconstruction error = anomaly
- **Feature extraction** — Use encoder output as features for downstream models
- **Denoising** — Denoising autoencoders learn to filter noise from financial data

### Generative Adversarial Networks (GANs)

Generator creates fake data, discriminator tries to distinguish real from fake. Both improve together.

**Use in finance:**
- Synthetic data generation for backtesting (especially for rare events)
- Market scenario generation
- Augmenting small datasets

---

## Practical Considerations

### What Works
| Application | Architecture | Success Level |
|-------------|-------------|---------------|
| NLP/Sentiment | Transformer (FinBERT) | High |
| Volatility forecasting | LSTM/GRU | Medium-High |
| Anomaly detection | Autoencoder | Medium-High |
| Feature extraction | Autoencoder, CNN | Medium |
| Return prediction | Any | Low-Medium |
| Portfolio optimization | RL + DL | Medium (research stage) |

### What Doesn't Work (Usually)
- Predicting next-day returns with deep learning on price data alone
- Complex architectures on small datasets (< 5 years daily data)
- Deep learning without proper financial cross-validation
- Using accuracy/MSE as the evaluation metric instead of Sharpe/P&L

### Training Tips for Finance
1. **Use purged k-fold CV** — Never let training data leak into test
2. **Embargo period** — Gap between train and test sets
3. **Early stopping** — Monitor validation loss, stop before overfitting
4. **Ensemble** — Average predictions from multiple models
5. **Feature importance** — Prune features that don't contribute
6. **Walk-forward retraining** — Retrain periodically on recent data
7. **Small models first** — Start simple, add complexity only if justified

---

## Key Libraries

| Library | Use |
|---------|-----|
| **PyTorch** | Primary DL framework (industry standard) |
| **TensorFlow/Keras** | Alternative DL framework |
| **HuggingFace** | Pre-trained NLP models (FinBERT) |
| **PyTorch Lightning** | Training boilerplate reduction |
| **Optuna** | Hyperparameter optimization |
| **Weights & Biases** | Experiment tracking |

---

## Related Notes
- [[ML and AI MOC]] — Parent note
- [[Supervised Learning]] — Classification and regression
- [[Reinforcement Learning]] — RL for trading
- [[Natural Language Processing (NLP)]] — NLP with deep learning
- [[Machine Learning Strategies]] — Strategy implementations
- [[Overfitting]] — The #1 enemy in financial DL
