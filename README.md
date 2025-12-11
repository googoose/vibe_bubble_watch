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
