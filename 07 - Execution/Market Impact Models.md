# Market Impact Models

Market impact models are used to estimate the price impact of a trade. This is a critical component of transaction cost analysis (TCA) and is essential for optimizing trade execution.

## Types of Market Impact Models

### Square Root Models
- **Formula:** `Market Impact = c * σ * sqrt(Q / V)`
    - `c`: A constant that depends on the market and the security.
    - `σ`: The volatility of the security.
    - `Q`: The size of the trade.
    - `V`: The average daily volume of the security.
- **Interpretation:** This is a simple and widely used model that assumes that market impact is proportional to the square root of the trade size relative to the average daily volume.

### Almgren-Chriss Model
- **Description:** A more sophisticated model that takes into account the trader's risk aversion and the temporary and permanent components of market impact.
- **Interpretation:** This model can be used to determine the optimal trading trajectory that minimizes a combination of market impact costs and risk.

## Factors that Affect Market Impact
- **Trade size:** Larger trades have a greater market impact.
- **Liquidity:** Trades in less liquid securities have a greater market impact.
- **Volatility:** Trades in more volatile securities have a greater market impact.
- **Trading style:** Aggressive trades that demand liquidity have a greater market impact than passive trades that provide liquidity.
