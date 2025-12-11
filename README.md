# AI Bubble Watch 🤖🫧

**AI Bubble Watch** is a professional Streamlit dashboard designed to monitor macro-economic risks and analyze the performance/valuation of AI-related stocks. It provides a comprehensive view of market breadth, liquidity stress, and leading economic indicators.

## 🚀 Features

The application is divided into three main analytical pillars:

### 1. Macro-Risk & Market Breadth ("Makro-Risiko")
*   **Liquidity Stress Monitor**: Real-time tracking of the **SOFR - DFF Spread**. A spread of >10bps signals potential liquidity stress in the overnight funding market.
*   **Shiller CAPE Ratio**: Visualizes current market valuation zones (Normal, Critical, Bubble) with color-coded alerts.
*   **Qualitative Risk**: "Vendor Financing" alerts to highlight qualitative risks often missed by quantitative models.

### 2. AI Stock Analysis & Benchmarking ("KI-Aktien-Analyse")
*   **Dynamic Stock Selection**: Search for any stock via Yahoo Finance and add it to your analysis dynamically.
*   **Performance Benchmarking**: Normalized 1-year performance charts to compare relative strength against indices like SPY.
*   **Valuation Radar**: Trailing P/E table with automatic EUR conversion and high-valuation warnings (>40x P/E).

### 3. Druckenmiller Indicators ("Druckenmiller Indikatoren")
Inspired by Stanley Druckenmiller's leading indicators for recession forecasting:
*   **Housing Market**: Monitors **Existing Home Sales** as a proxy for consumer confidence and interest rate sensitivity.
*   **Trucking & Freight**: Tracks **Truck Tonnage** as a real-time measure of industrial production and physical goods demand.
*   **Combined Signal**: Aggregates trends to provide a "Macro Traffic Light" (Green/Yellow/Red).

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/)
*   **Data**: 
    *   [FRED API](https://fred.stlouisfed.org/docs/api/fred/) (Federal Reserve Economic Data)
    *   [yfinance](https://pypi.org/project/yfinance/) (Yahoo Finance)
*   **Visualization**: Plotly & Antigravity UI components

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd vibe_bubble_watch
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    You need a FRED API Key to fetch economic data.
    *   Create a `.env` file in the root directory.
    *   Add your API key:
        ```bash
        FRED_API_KEY=your_fred_api_key_here
        ```
    *   *Alternatively, the app will try to load `st.secrets` if deployed on Streamlit Cloud.*

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

## ⚠️ Disclaimer

This tool is for **informational and educational purposes only**. It does not constitute financial advice. All data is provided "as is" via third-party APIs (FRED, Yahoo Finance).