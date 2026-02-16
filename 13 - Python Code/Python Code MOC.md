# Python Code — Map of Content

> The quant's primary weapon. Python isn't the fastest language, but its ecosystem for data analysis, ML, and prototyping is unmatched.

---

## Core Libraries

### Data & Computation
| Library         | Use                                | Import                              |
| --------------- | ---------------------------------- | ----------------------------------- |
| **NumPy**       | Numerical computing, arrays        | `import numpy as np`                |
| **Pandas**      | DataFrames, time series            | `import pandas as pd`               |
| **SciPy**       | Scientific computing, optimization | `from scipy import optimize, stats` |
| **Statsmodels** | Econometrics, time series models   | `import statsmodels.api as sm`      |

### Visualization
| Library | Use | Import |
|---------|-----|--------|
| **Matplotlib** | Base plotting | `import matplotlib.pyplot as plt` |
| **Seaborn** | Statistical plots | `import seaborn as sns` |
| **Plotly** | Interactive charts | `import plotly.graph_objects as go` |

### Machine Learning
| Library | Use | Import |
|---------|-----|--------|
| **Scikit-learn** | Classical ML | `from sklearn.ensemble import RandomForestClassifier` |
| **XGBoost** | Gradient boosting | `import xgboost as xgb` |
| **LightGBM** | Fast gradient boosting | `import lightgbm as lgb` |
| **PyTorch** | Deep learning | `import torch` |

### Finance-Specific
| Library | Use | Import |
|---------|-----|--------|
| **yfinance** | Yahoo Finance data | `import yfinance as yf` |
| **ccxt** | Crypto exchange API | `import ccxt` |
| **QuantLib** | Derivatives pricing | `import QuantLib as ql` |
| **zipline** | Backtesting framework | `from zipline import run_algorithm` |
| **backtrader** | Backtesting framework | `import backtrader as bt` |
| **vectorbt** | Fast vectorized backtesting | `import vectorbt as vbt` |
| **hmmlearn** | Hidden Markov Models | `from hmmlearn.hmm import GaussianHMM` |

### Data & APIs
| Library | Use | Import |
|---------|-----|--------|
| **requests** | HTTP requests | `import requests` |
| **websocket** | WebSocket connections | `import websocket` |
| **alpaca-trade-api** | Alpaca broker API | `import alpaca_trade_api as tradeapi` |
| **ibapi** | Interactive Brokers API | `from ibapi.client import EClient` |

---

## Code Templates

### Quick Data Download
```python
import yfinance as yf
import pandas as pd

# Download historical data
data = yf.download(['AAPL', 'MSFT', 'GOOGL'], start='2020-01-01')
prices = data['Adj Close']
returns = prices.pct_change().dropna()
```

### Quick Backtest Template
```python
import numpy as np
import pandas as pd

def simple_backtest(prices, signals, initial_capital=100000, commission=0.001):
    """
    Vectorized backtest template.

    Parameters:
        prices: pd.Series or DataFrame of prices
        signals: pd.Series or DataFrame of position sizes (-1 to 1)
        commission: Proportional commission
    """
    returns = prices.pct_change()
    strategy_returns = signals.shift(1) * returns  # Shift to avoid lookahead

    # Transaction costs
    turnover = signals.diff().abs()
    costs = turnover * commission
    net_returns = strategy_returns - costs

    # Performance
    cumulative = (1 + net_returns).cumprod() * initial_capital
    total_return = cumulative.iloc[-1] / initial_capital - 1
    sharpe = net_returns.mean() / net_returns.std() * np.sqrt(252)
    max_dd = (cumulative / cumulative.cummax() - 1).min()

    return {
        'equity_curve': cumulative,
        'total_return': total_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'annual_return': (1 + total_return) ** (252 / len(returns)) - 1
    }
```

---

## Strategy Code (Embedded in Notes)
- Simple Moving Average Crossover — See [[Momentum Strategies]]
- Pairs Trading (Z-score) — See [[Statistical Arbitrage]]
- Market Making (Avellaneda-Stoikov) — See [[Market Making Strategies]]
- Mean Reversion (Bollinger) — See [[Mean Reversion Strategies]]
- Monte Carlo Simulation — See [[Monte Carlo Simulation]]
- Factor Portfolio Construction — See [[Factor Investing]]
- Black-Litterman — See [[Black-Litterman Model]]
- Mean-Variance Optimization — See [[Modern Portfolio Theory]]
- HRP Portfolio — See [[Portfolio Optimization]]
- HMM Regime Detection — See [[Regime Detection]]
- Cointegration Testing — See [[Cointegration]]
- LSTM Price Prediction — See [[Deep Learning]]
- Transformer Model — See [[Deep Learning]]
- Alpha Signal Construction — See [[Alpha Research]]

---

## Related Notes
- [[Trading Algorithms Master Index]] — Master vault index
- [[Backtesting MOC]] — Backtesting frameworks
- [[Data Engineering MOC]] — Data pipelines
- [[ML and AI MOC]] — ML libraries and code
