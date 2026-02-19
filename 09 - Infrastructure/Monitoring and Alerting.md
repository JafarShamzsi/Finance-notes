# Monitoring and Alerting

For an algorithmic trading desk, monitoring is not just about "server health" — it is about ensuring the strategy is behaving as expected and the system is not losing money due to technical errors.

---

## 1. Three Layers of Monitoring

### A. System Infrastructure (IT Health)
- **Metrics:** CPU usage, RAM (leaks), Disk I/O, Network Latency.
- **Tools:** Prometheus, Grafana, Datadog.
- **Critical Alert:** "Trading Server unreachable" or "Market Data Link down."

### B. Execution & Order Flow
- **Metrics:** Fill rates, Reject rates, Message count (throttling), Late ticks.
- **Latency Monitoring:** Tick-to-Trade latency (How long did the "brain" take?).
- **Critical Alert:** "Fill rate dropped below 50%" or "Exchange rejecting all orders."

### C. Strategy & P&L (The Quant View)
- **Metrics:** Current P&L (Realized vs. Unrealized), Position size vs. Limits, Drawdown.
- **Drift Detection:** Does the live P&L match the theoretical P&L from the simulator?
- **Critical Alert:** "Maximum Daily Loss reached" or "Strategy position exceeds risk limit."

---

## 2. Dashboarding with Grafana

A typical Quant dashboard includes:
1.  **Equity Curve:** Real-time P&L for the day.
2.  **Order Book Heatmap:** Visualizing liquidity depth.
3.  **Latency Histograms:** Monitoring the 99th percentile (tail) latency.
4.  **Log Feed:** Tail of the system logs for warning messages.

---

## 3. Alerting Strategies

Alerts must be **Actionable**.
- **Critical (PagerDuty/SMS):** Immediate intervention required. System is "Bleeding."
- **Warning (Slack/Email):** Non-urgent issue. Investigate during market hours.
- **Informational:** Periodic stats. No immediate action.

---

## 4. The "Kill Switch"

The most important feature of any monitoring system is the **Kill Switch**.
- **Manual Kill:** A big red button on the dashboard to flatten all positions and stop the system.
- **Automatic Kill:** The monitoring system triggers a shutdown if:
    - P&L drops below a "Hard Stop" threshold.
    - The connection to the exchange is unstable.
    - The system detects a "Logic Loop" (sending orders too fast).

---

## 5. Post-Trade Analysis (T+1)

Daily "Health Check" reports:
- **Slippage Report:** Are we getting worse fills than expected? (See [[Transaction Cost Analysis (TCA)]]).
- **Reconciliation:** Do our internal position records match the broker's records?

---

## Related Notes
- [[Trading System Architecture]] — Where metrics are generated
- [[Risk Management MOC]] — Logic for kill switches
- [[Transaction Cost Analysis (TCA)]] — Analyzing performance
- [[Performance Metrics]] — What we are measuring
- [[Infrastructure MOC]] — System design
