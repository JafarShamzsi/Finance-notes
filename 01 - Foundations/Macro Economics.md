# Macro Economics for Quants

Macroeconomics is the study of economy-wide phenomena, including inflation, price levels, rate of economic growth, national income, gross domestic product (GDP), and changes in unemployment. For quants, macro data provides the "context" for market regimes and is the primary driver of **Forex** and **Fixed Income** strategies.

---

## 1. Key Macro Indicators

| Indicator | Significance | Typical Impact |
|-----------|--------------|----------------|
| **GDP (Gross Domestic Product)** | Overall economic health. | High GDP = Bullish for Equities, Bearish for Bonds (inflation risk). |
| **CPI (Consumer Price Index)** | Measures inflation. | High CPI = Central Bank hikes rates = Bullish for Currency, Bearish for Bonds. |
| **NFP (Non-Farm Payrolls)** | US employment health. | The most volatile event for USD and US Equities. |
| **PMI (Purchasing Managers' Index)** | Manufacturing/Services sentiment. | Leading indicator of economic expansion/contraction. |

---

## 2. Central Bank Policy (Monetary Policy)

Central banks (The Fed, ECB, BOJ) control the money supply and short-term interest rates.

- **Hawkish:** Policy favoring higher interest rates to combat inflation. (Bullish for currency).
- **Dovish:** Policy favoring lower interest rates to stimulate growth. (Bearish for currency).
- **Quantitative Easing (QE):** Increasing money supply by buying bonds (lowers yields).
- **Quantitative Tightening (QT):** Decreasing money supply by selling bonds (raises yields).

---

## 3. Global Macro Drivers

### A. Interest Rate Parity (IRP)
The theory that the difference in interest rates between two countries should equal the difference between the forward exchange rate and the spot exchange rate. (See [[FX Trading]]).

### B. Yield Curve Spreads
The difference between long-term and short-term rates (e.g., 2s10s spread). An **inverted yield curve** is a historically reliable predictor of a recession.

### C. Terms of Trade
The ratio of export prices to import prices. Critical for **Commodity Currencies** (AUD, CAD, NOK).

---

## 4. Quantitative Macro (Systematic Macro)

Modern macro quants don't just "read news"; they build models to ingest data automatically:
- **Nowcasting:** Using high-frequency data (shipping, retail traffic) to estimate GDP before official releases.
- **Sentiment Analysis:** Using NLP on FOMC minutes to determine hawkish/dovish shifts (see [[Natural Language Processing (NLP)]]).
- **Relative Value Macro:** Trading the spread between countries based on diverging macro fundamentals.

---

## 5. Event Risk Management

Macro events create "gaps" in liquidity.
- **Economic Calendar:** Quants must monitor scheduled releases.
- **Sizing Down:** Reducing risk exposure ahead of major binary events (like an FOMC meeting).

---

## Related Notes
- [[FX Trading]] — Primary macro application
- [[Fixed Income]] — Rate-driven asset class
- [[Regime Detection]] — Macro regimes
- [[Alternative Data]] — Used for nowcasting
- [[Natural Language Processing (NLP)]] — Analyzing central bank speech
