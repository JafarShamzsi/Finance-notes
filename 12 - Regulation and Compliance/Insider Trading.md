# Insider Trading

Trading on **Material Non-Public Information (MNPI)**. One of the most seriously prosecuted securities violations.

---

## What Constitutes Insider Trading

### Material Information
Information that a **reasonable investor** would consider important in making an investment decision:
- Earnings results (before announcement)
- M&A activity (before announcement)
- FDA approval/rejection
- Major contract wins/losses
- Regulatory actions
- Material cybersecurity breaches

### Non-Public
Information not yet disseminated to the general public through official channels (press releases, SEC filings, earnings calls).

---

## Legal Framework

### Securities Exchange Act Section 10(b) + Rule 10b-5
- Prohibits fraud and deception in connection with securities trading
- Basis for most insider trading prosecutions

### Insider Trading Sanctions Act (1984)
- Civil penalties up to **3x profits gained** or losses avoided

### Insider Trading and Securities Fraud Enforcement Act (1988)
- Criminal penalties: up to **$5M fine** and **20 years prison** for individuals
- Firms can be fined up to **$25M**

---

## Theories of Liability

| Theory | Who's Liable | Basis |
|--------|-------------|-------|
| **Classical** | Corporate insiders (officers, directors) | Breach of fiduciary duty to shareholders |
| **Tipper-Tippee** | Person who tips + person who trades | Tipper breached duty for personal benefit |
| **Misappropriation** | Anyone who misappropriates confidential info | Breach of duty to the source of information |

---

## Relevance to Quant Trading

### Alternative Data Risks
- **Web scraping** — Scraping non-public data could be MNPI if from insiders
- **Satellite data** — Generally legal (public observation), but edge cases exist
- **Credit card data** — Aggregated = OK, individual company = potential MNPI
- **Expert networks** — High risk of receiving MNPI from industry experts
- **Social media** — Public posts are fine; private messages from insiders are not

### Information Barriers (Chinese Walls)
At JPM/Goldman, strict information barriers separate:
- Investment banking (has MNPI) from trading (must not receive MNPI)
- Research from proprietary trading
- Different client accounts

**Algo teams must ensure** their data sources don't contain MNPI. Compliance reviews alternative data vendors.

---

## Notable Cases

| Case | Year | Outcome |
|------|------|---------|
| Raj Rajaratnam (Galleon) | 2011 | 11 years prison, $150M+ penalties |
| SAC Capital (Steve Cohen) | 2013 | $1.8B fine, fund renamed Point72 |
| Martha Stewart | 2004 | 5 months prison (obstruction, not insider trading) |
| Mathew Martoma (SAC) | 2014 | 9 years prison |

---

## Related Notes
- [[Market Manipulation]] — Other forms of market misconduct
- [[Regulation and Compliance MOC]] — Parent note
- [[Alternative Data]] — Data source compliance
- [[SEC and FINRA Rules]] — Legal framework
