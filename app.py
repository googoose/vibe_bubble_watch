import streamlit as st
import pandas as pd
import yfinance as yf
from fredapi import Fred
import antigravity as ag
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Configuration
ag.set_page_config(theme='dark')

st.title("AI Bubble Watch")


# 2. Data Fetching & Caching

@st.cache_data(ttl=86400)
def get_fred_data(api_key):
    """
    Fetches DFF and SOFR data from FRED.
    """
    try:
        if not api_key:
            raise ValueError("FRED API Key is missing.")
        
        fred = Fred(api_key=api_key)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*3) # Fetch 3 years for context
        
        # Fetch data
        dff = fred.get_series('DFF', observation_start=start_date, observation_end=end_date)
        sofr = fred.get_series('SOFR', observation_start=start_date, observation_end=end_date)
        housing = fred.get_series('EXHOSLUSM495S', observation_start=start_date, observation_end=end_date)
        trucking = fred.get_series('TSIFRGHT', observation_start=start_date, observation_end=end_date)
        
        # Combine into DataFrame
        df = pd.DataFrame({
            'DFF': dff, 
            'SOFR': sofr,
            'Housing': housing,
            'Trucking': trucking
        })
        # Forward fill to handle different frequencies (Housing/Trucking are monthly)
        df.ffill(inplace=True)
        df.dropna(inplace=True)
        
        # Calculate Spread (in Basis Points)
        df['Spread_Bps'] = (df['SOFR'] - df['DFF']) * 100
        
        return df
    except Exception as e:
        st.error(f"Error fetching FRED data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_stock_data(tickers):
    """
    Fetches historical price data for selected tickers.
    """
    try:
        if not tickers:
            return pd.DataFrame()
            
        data = yf.download(tickers, period="1y", auto_adjust=True, progress=False)['Close']
        
        if data.empty:
            return pd.DataFrame()
            
        return data
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_valuation_data(tickers):
    """
    Fetches Trailing P/E and Current Price (converted to EUR) for selected tickers.
    """
    valuation_data = []
    
    # Fetch EURUSD rate for conversion
    try:
        eur_usd = yf.Ticker("EURUSD=X").info.get('regularMarketPrice', 1.05) # Fallback if fails
        if not eur_usd or eur_usd == 0: eur_usd = 1.05 # Safety
    except:
        eur_usd = 1.05

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe = info.get('trailingPE', None)
            price = info.get('currentPrice', info.get('regularMarketPrice', None))
            currency = info.get('currency', 'USD')
            
            # Convert to EUR if necessary
            price_eur = price
            if price and currency == 'USD':
                # USD / EURUSD_Rate = EUR? No. EURUSD=X is 1 Euro = X USD. 
                # So USD / Rate = Euro. example: 100 USD / 1.05 = 95 EUR.
                price_eur = price / eur_usd
            elif price and currency != 'EUR':
                # Fallback for other currencies: leave as is or basic approximation?
                # For now assuming mostly USD stocks in this list. 
                pass
                
            valuation_data.append({
                'Ticker': ticker, 
                'Price (€)': round(price_eur, 2) if price_eur else None,
                'Trailing P/E': pe
            })
        except Exception as e:
            # Quietly ignore individual ticker errors for valuation to avoid spamming UI
            valuation_data.append({'Ticker': ticker, 'Price (€)': None, 'Trailing P/E': None})
            
    return pd.DataFrame(valuation_data)

# 3. UI Layout & Logic

tab1, tab2, tab3 = st.tabs(["Makro-Risiko & Marktbreite", "KI-Aktien-Analyse & Benchmarking", "Druckenmiller Indikatoren"])

# --- Tab 1: Makro-Risiko ---
with tab1:
    st.header("Makro-Risiko Indikatoren")
    
    # FRED Data
    # Try to get API key from secrets or env, else use provided key
    api_key = os.environ.get('FRED_API_KEY')
    if not api_key:
        try:
            api_key = st.secrets["FRED_API_KEY"]
        except:
            pass
            
    if not api_key:
        st.warning("FRED API Key not found. Please set FRED_API_KEY environment variable.")

    
    fred_df = get_fred_data(api_key)
    
    if not fred_df.empty:
        ag.chart(
            fred_df[['Spread_Bps']].iloc[-365:], 
            title="SOFR - DFF Spread (Basispunkte)",
            hline=10,
            hline_color="red",
            hline_label="Stress-Level (10 bps)"
        )
        with st.expander("Interpretation", expanded=True):
            st.write("""
            Der Spread (SOFR - DFF) in Basispunkten. 
            **Warnung:** Ein Spread von **10 Basispunkten oder mehr** (rote Linie) wird als ein sehr ernstes Anzeichen von Liquiditätsstress 
            im besicherten Übernachtungsmarkt gewertet, der potenziell eine Reaktion der Federal Reserve auslösen könnte.
            """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Shiller CAPE Ratio")
        cape_value = 39.42
        
        # Color Logic
        if cape_value > 30:
            cape_color = "#FF4B4B" # Red
        elif cape_value > 25:
            cape_color = "#FFC107" # Yellow
        else:
            cape_color = "#4CAF50" # Green
            
        ag.card(title="Current Shiller CAPE", value=str(cape_value), color=cape_color)
        
        with st.expander("Bewertung & Bedeutung"):
            st.markdown("""
            | Zustand | Kritische Schwelle | Bedeutung |
            | :--- | :--- | :--- |
            | **Normal** | 15 – 20 | Signalisiert faire Bewertungen und historisch übliche langfristige Renditen. |
            | **Kritisch** | Über 25 | Signalisiert deutliche Überbewertung und **unterdurchschnittliche** langfristige Renditen. |
            | **Blase** | **Über 30 – 35** | **Hochspekulative Blase.** Werte in dieser Region wurden nur extrem selten erreicht. |
            """)
        
    with col2:
        st.subheader("Qualitative Risiko-Analyse")
        ag.markdown("""
        ### :warning: Vendor Financing Risk
        **Achtung:** Es besteht ein erhöhtes Risiko durch "Vendor Financing" (Kundenfinanzierung). 
        Große Tech-Unternehmen finanzieren möglicherweise ihre eigenen Kunden, um Umsätze künstlich aufzublähen ("Funny Money").
        Dies ist ein qualitativer Faktor, der in quantitativen Modellen oft übersehen wird.
        """)

# --- Tab 2: KI-Aktien-Analyse ---
with tab2:
    st.header("KI-Aktien Performance & Bewertung")
    
    # Initialize session state for tickers if not present
    if 'ticker_list' not in st.session_state:
        st.session_state['ticker_list'] = ['NVDA', 'MSFT', 'GOOGL', 'SPY', 'XLP']
    
    # Initialize session state for SELECTED tickers if not present
    # This allows us to programmatically update the selection
    if 'selected_tickers' not in st.session_state:
        st.session_state['selected_tickers'] = ['NVDA', 'MSFT', 'GOOGL', 'SPY', 'XLP']

    # --- Stock Search Functionality ---
    import requests
    
    @st.cache_data(ttl=3600)
    def search_yahoo(query):
        try:
            url = "https://query2.finance.yahoo.com/v1/finance/search"
            headers = {'User-Agent': 'Mozilla/5.0'}
            params = {'q': query, 'quotesCount': 5, 'newsCount': 0}
            r = requests.get(url, headers=headers, params=params)
            data = r.json()
            if 'quotes' in data:
                return [(q['symbol'], q.get('shortname', q.get('longname', ''))) for q in data['quotes'] if 'symbol' in q]
            return []
        except:
            return []

    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Aktie suchen (z.B. Palantir):", key="stock_search")
    
    search_results = []
    if len(search_query) > 2:
        search_results = search_yahoo(search_query)
    
    with col2:
        # If we have results, show a selectbox to pick one
        if search_results:
            # Create options list like "PLTR - Palantir Technologies Inc."
            options = [f"{s[0]} - {s[1]}" for s in search_results]
            selected_option = st.selectbox("Ergebnisse:", options, label_visibility="collapsed")
            
            if st.button("Hinzufügen"):
                # Extract symbol
                symbol = selected_option.split(" - ")[0]
                
                # Add to options list if not present
                if symbol not in st.session_state['ticker_list']:
                    st.session_state['ticker_list'].append(symbol)
                
                # Add to SELECTED list if not present
                if symbol not in st.session_state['selected_tickers']:
                    st.session_state['selected_tickers'].append(symbol)
                    st.success(f"{symbol} hinzugefügt & ausgewählt!")
                    st.rerun()
                else:
                    st.warning("Aktie bereits ausgewählt.")
        else:
            st.write("") # Spacer

    # Multiselect with dynamic options and programmatic selection
    # We use key='selected_tickers' to bind it to session state
    selected_tickers = st.multiselect(
        "Wähle Aktien/ETFs:", 
        options=st.session_state['ticker_list'],
        key='selected_tickers'
    )
    
    if selected_tickers:
        # Performance Chart
        stock_df = get_stock_data(selected_tickers)
        
        if not stock_df.empty:
            # Normalize to 100
            normalized_df = stock_df / stock_df.iloc[0] * 100
            ag.chart(normalized_df, title="Relative Performance (Start = 100)")
        
        # Valuation Table
        st.subheader("Bewertung (Trailing P/E)")
        val_df = get_valuation_data(selected_tickers)
        
        if not val_df.empty:
            # Set index for better display
            val_df.set_index('Ticker', inplace=True)
            
            def highlight_high_pe(val):
                color = 'red' if val is not None and val > 40 else ''
                return f'color: {color}'
            
            ag.table(val_df, highlight_cols=['Trailing P/E'], highlight_func=highlight_high_pe)
    else:
        st.info("Bitte wähle mindestens eine Aktie aus.")

# --- Tab 3: Druckenmiller Indikatoren ---
with tab3:
    st.header("Druckenmiller Indikatoren (Housing & Trucking)")
    st.write("Frühindikatoren für die Konjunktur, inspiriert von Stanley Druckenmiller.")
    
    if not fred_df.empty and 'Housing' in fred_df.columns and 'Trucking' in fred_df.columns:
        # --- Logic Calculation ---
        # Get latest values
        latest_housing = fred_df['Housing'].iloc[-1]
        latest_trucking = fred_df['Trucking'].iloc[-1]
        
        # Get values 1 year ago (approx 252 trading days or 12 months)
        # Using 252 for daily data approximation if index is daily
        # Since we ffilled, we have daily rows.
        one_year_ago_idx = -252 if len(fred_df) > 252 else 0
        
        housing_1y = fred_df['Housing'].iloc[one_year_ago_idx]
        trucking_1y = fred_df['Trucking'].iloc[one_year_ago_idx]
        
        # Calc Trends
        housing_trend = (latest_housing / housing_1y) - 1
        trucking_trend = (latest_trucking / trucking_1y) - 1
        
        # Signal Logic
        signal_color = "#4CAF50" # Green default
        signal_text = "Stabil / Positiv"
        
        if housing_trend < 0 and trucking_trend < 0:
            signal_color = "#FF4B4B" # Red (using Red/Orange tone for warning)
            signal_text = "Vorsicht: Abschwächung der Zukunfts- und Produktionsnachfrage"
        elif housing_trend < 0 or trucking_trend < 0:
            signal_color = "#FFC107" # Yellow
            signal_text = "Vorsicht: Gemischte Signale"

        # --- Aggregation Card ---
        # Using custom HTML for the top card to match ag.card style but full width
        st.markdown(f"""
            <div style="background-color: {signal_color}; padding: 15px; border-radius: 10px; text-align: center; color: black; margin-bottom: 20px; border: 1px solid #464B5C;">
                <h3 style="margin:0;">Gesamtkonjunktur-Signal: {signal_text}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # --- Columns ---
        col_housing, col_trucking = st.columns(2)
        
        with col_housing:
            st.subheader("Housing: Zins- & Konsumenten-Vertrauens-Signal")
            ag.card("Latest New Home Sales", f"{latest_housing:,.0f}")
            st.metric("1-Year Trend", f"{housing_trend:.1%}", delta_color="normal" if housing_trend >= 0 else "inverse")
            ag.chart(fred_df[['Housing']].iloc[-756:], title="Bestehende Hausverkäufe (Sinkende Käufernachfrage)") 
            
        with col_trucking:
            st.subheader("Trucking: Reales Produktions- & Fracht-Signal")
            ag.card("Latest Freight Index", f"{latest_trucking:.2f}")
            st.metric("1-Year Trend", f"{trucking_trend:.1%}", delta_color="normal" if trucking_trend >= 0 else "inverse")
            ag.chart(fred_df[['Trucking']].iloc[-756:], title="Fracht-Index (Nachlassende Industrieproduktion)")
            
    else:
        st.warning("Housing & Trucking Daten konnten nicht geladen werden.")

    # --- Explanatory Tables ---
    st.markdown("---")
    st.subheader("Erklärung der Indikatoren")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("**Housing Indikatoren**")
        st.markdown("""
        | Indikator | Was er misst | Aussage bei Schwäche (Fallen) |
        | :--- | :--- | :--- |
        | **Existing-Home Sales**<br>(Bestehende Hausverkäufe) | Wie viele Häuser den Besitzer wechseln. | Die **Nachfrage der Käufer** bricht ein, oft durch hohe Zinsen oder mangelndes Vertrauen in die Zukunft. |
        | **Building Permits**<br>(Baugenehmigungen) | Wie viele neue Bauprojekte geplant sind. | **Bauunternehmen** verlieren das Vertrauen in die zukünftige Nachfrage. Dies deutet auf einen **zukünftigen Rückgang** der Bautätigkeit und der Bau-Jobs hin. |
        """)
        
    with col_info2:
        st.markdown("**Trucking & Freight Indikatoren**")
        st.markdown("""
        | Indikator | Was er misst | Aussage bei Schwäche (Fallen) |
        | :--- | :--- | :--- |
        | **Truck Tonnage Index**<br>(Tonnage Index) | Das Gesamtgewicht der transportierten Fracht. | Die **Produktion und der Konsum** in der Gesamtwirtschaft lassen nach. Wenn weniger Waren transportiert werden, werden auch weniger Waren produziert oder bestellt. |
        | **Freight Services Index (TSI)** | Ein breiteres Maß für die gesamte Frachtaktivität (Straße, Schiene, Luft). | Bestätigt den Rückgang der Tonnage und deutet auf eine **breitere Verlangsamung** der Lieferketten hin. |
        """)

