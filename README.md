<<<<<<< HEAD
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
=======
## 🫧 AI Bubble Watch: Macro-Risk & Stock Analysis Dashboard

This project, **AI Bubble Watch**, is an interactive dashboard designed to monitor potential **macro-risks** in the market and perform **in-depth analysis** of stocks associated with the AI industry. It serves as a central tool for investors and analysts seeking data-driven insights into market sentiment and specific stock valuations.

---

### ✨ Features

The dashboard provides a range of indicators and analyses to give a comprehensive view of the market situation:

#### 📈 Macro-Risk Indicators

* **SOFR-DFF Spread:** Monitoring the difference between the Secured Overnight Financing Rate and the Effective Federal Funds Rate as an indicator of liquidity and stress levels in the banking system.
* **Shiller CAPE (Cyclically Adjusted Price-to-Earnings Ratio):** Assessing stock market overvaluation in a historical context.
* **Vendor Financing:** Analysis of trends in vendor financing as a potential early warning sign of economic downturns or excessive risk-taking.

#### 🤖 AI Stock Analysis

* **Performance Tracking:** Tracking the historical and current performance of selected AI-relevant stocks.
* **Valuation (P/E):** Calculation and display of the Price-to-Earnings ratio (P/E) to assess current valuation.
* **Dynamic Search:** Interactive search function to add and analyze specific stocks.

#### 🚛 Druckenmiller Indicators

* **Housing & Trucking Economic Signals:** Integration of John Druckenmiller's preferred indicators for assessing overall economic strength, particularly in the housing and trucking sectors.

### 🛠️ Tech Stack

The project relies on the following technologies and libraries:

| Component | Purpose | Libraries/Tools |
| :--- | :--- | :--- |
| **Frontend/App** | Interactive Dashboard | Streamlit |
| **Data Processing** | Data management and analysis | Python, Pandas |
| **Financial Data** | Stock data, P/E ratio | `yfinance` |
| **Economic Data** | Macro indicators (SOFR, etc.) | `FRED API` |

---

### ⚙️ Installation

Follow these steps to set up and run the application locally:

#### 1. Clone the Repository

Open your terminal or command prompt and clone the repository:

```bash
git clone [YOUR_REPO_URL]
cd AI_Bubble_Watch
````

#### 2. Install Dependencies
Install all required Python packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

#### 3. Environment Setup
You will need an API key from the Federal Reserve Bank of St. Louis (FRED) to access the macro-risk data.

Get your key from the FRED website.

Create a file named .env in the root directory of the project.

Add your key to the .env file in the following format:

```bash
FRED_API_KEY="YOUR_PERSONAL_FRED_API_KEY
```
#### ▶️ Usage
Start the Streamlit dashboard by running the following command in the project's root directory:
```bash
streamlit run app.py
```
The application will open in your default web browser.

⚠️ Disclaimer
This is not a financial product and does not constitute investment advice. The data and analyses provided in this tool are strictly for informational and educational purposes only. Past performance is not an indicator of future results. Do not make investment decisions based on this dashboard without independent, professional consultation. The developer assumes no liability for losses or damages arising from the use of this information.
>>>>>>> 1c898cee98a2780338771cf01010fe23eb2d0468
