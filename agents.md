# AI Bubble Watch - Agents Definition

This document defines the autonomous agents and their roles within the **AI Bubble Watch** ecosystem. These definitions can be used to configure multi-agent systems or simply to understand the logical separation of concerns in the application.

---

## 1. Market Data Collector
**Role:** Data Engineer  
**Goal:** Reliable acquisition of financial time-series data.  
**Tools:** `fredapi`, `yfinance`

**Responsibilities:**
- Fetch daily **SOFR** and **DFF** rates from the FRED API.
- Download historical price data for selected AI stocks (e.g., NVDA, MSFT) and benchmarks (SPY).
- Retrieve fundamental valuation metrics (Trailing P/E).
- **Caching:** Maintain a local cache (TTL 24h for Macro, 1h for Stocks) to minimize API calls.
- **Error Handling:** Gracefully handle API timeouts and missing data points (return empty DataFrames).

## 2. Risk Analyst
**Role:** Financial Analyst  
**Goal:** Identify market anomalies and valuation risks.  
**Tools:** `pandas`, `numpy`

**Responsibilities:**
- **Spread Analysis:** Calculate the spread between SOFR and DFF to detect interbank stress.
- **Valuation Check:** Compare current P/E ratios against a threshold (e.g., > 40x).
- **Bubble Detection:** Monitor parabolic price moves (normalized performance > 200% in 1y).
- **Qualitative Assessment:** Flag non-quantifiable risks like "Vendor Financing" or "Funny Money".

## 3. UI Host (Antigravity)
**Role:** Frontend Developer  
**Goal:** Present complex data in a simplified, professional "Dark Mode" interface.  
**Tools:** `streamlit`, `plotly`, `antigravity` wrapper

**Responsibilities:**
- **Visualization:** Render interactive charts for Spreads and Stock Performance.
- **Alerting:** Display prominent warnings (Red Text/Icons) for high-risk indicators.
- **User Interaction:** Handle user inputs (Stock Search, Ticker Selection) via Session State.
- **Aesthetics:** Enforce the "Antigravity" design language (Dark theme, Card layouts).

---

## Workflow Interaction

1.  **User** initiates a request (loads app or searches ticker).
2.  **UI Host** requests data from **Market Data Collector**.
3.  **Market Data Collector** fetches/retrieves data and passes it to **Risk Analyst**.
4.  **Risk Analyst** processes data (calculates spreads, flags high P/E) and returns insights.
5.  **UI Host** renders the final view to the **User**.
