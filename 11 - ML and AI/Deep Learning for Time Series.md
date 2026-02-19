# Deep Learning for Time Series

While classical econometrics (ARIMA, GARCH) models linear dependencies, **Deep Learning (DL)** allows quants to capture high-dimensional, non-linear relationships in market data. In modern trading, DL is primarily used for **Volatility Forecasting**, **Order Flow Modeling**, and **Alpha Generation** from unstructured or complex structured data.

---

## 1. Why Time Series is Different

Unlike computer vision or NLP, financial time series have:
- **Low Signal-to-Noise Ratio (SNR):** Most variance is noise.
- **Non-Stationarity:** The underlying data-generating process changes (regime shifts).
- **Adversarial Nature:** Markets adapt to known patterns, causing alpha decay.

---

## 2. Core Architectures for Finance

### A. Recurrent Neural Networks (RNNs) & LSTM/GRU
Designed for sequential data. **LSTMs (Long Short-Term Memory)** use gates to manage "memory," allowing them to capture long-term dependencies (e.g., a trend that started weeks ago) without the vanishing gradient problem.
- **Use Case:** Predicting the next log-return or volatility state.

### B. Convolutional Neural Networks (CNNs) 
Though famous for images, 1D-CNNs are excellent for financial time series. They act as automated "Technical Indicator" discoverers, learning optimal filters for price patterns.
- **Use Case:** Chart pattern recognition and feature extraction from Limit Order Books (LOB).

### C. Transformers & Attention Mechanisms
The "Attention" mechanism allows the model to focus on specific past events that are relevant to the current state, regardless of their chronological distance.
- **Informer/Temporal Fusion Transformer (TFT):** Modern variants specifically designed for multi-horizon time series forecasting.

---

## 3. Advanced Input Representations

Feeding raw prices into a neural network is rarely successful.

| Representation | Description | Benefit |
|----------------|-------------|---------|
| **Fractional Differentiation** | Preserving memory while achieving stationarity. | Keeps price level info without random walk noise. |
| **Wavelet Transforms** | Decomposing time series into time-frequency space. | Isolates short-term noise from long-term trends. |
| **Gramian Angular Fields (GAF)** | Converting 1D time series into 2D images. | Allows the use of powerful 2D-CNN architectures. |
| **LOB Snapshots** | 2D representation of price levels and volumes. | Captures microstructure state. |

---

## 4. Loss Functions for Trading

Standard Mean Squared Error (MSE) is often suboptimal for finance because it doesn't distinguish between "missing the magnitude" and "missing the direction."

- **Directional Loss:** Penalizing the model more when it predicts the wrong sign of the return.
- **Sharpe Loss:** Directly optimizing for the Sharpe ratio of the resulting strategy.
- **Quantile Loss:** Used for Value-at-Risk (VaR) forecasting to estimate the "tails" of the distribution.

---

## 5. Training Strategy: The "Quant Way"

1.  **Normalization:** Use **Z-Score** or **Quantile Transforms** on a rolling window to avoid look-ahead bias.
2.  **Regularization:** Heavy use of **Dropout** and **L1/L2 penalties** is mandatory due to the noise in financial data.
3.  **Ensembling:** Averaging the predictions of 10-20 models with different random seeds or architectures to reduce variance.
4.  **Transfer Learning:** Pre-training a model on a large universe of liquid stocks before fine-tuning it on a specific asset class.

---

## 6. Implementation Sketch (PyTorch LSTM)

```python
import torch
import torch.nn as nn

class AlphaLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers=2):
        super(AlphaLSTM, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, 1) # Output: Predicted Return

    def forward(self, x):
        # x shape: (batch, seq_len, input_dim)
        out, _ = self.lstm(x)
        # Take the hidden state of the last time step
        last_step_out = out[:, -1, :]
        prediction = self.fc(last_step_out)
        return prediction
```

---

## Related Notes
- [[Deep Learning]] — General foundations.
- [[Machine Learning Strategies]] — How to build strategies with these models.
- [[Feature Engineering for Trading]] — Preparing inputs for DL.
- [[Regime Detection]] — Using DL to identify market states.
- [[Time Series Analysis]] — Classical benchmarks.
