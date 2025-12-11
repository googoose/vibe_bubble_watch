import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def set_page_config(theme='dark'):
    """
    Sets the page config. 
    Note: Streamlit's theme is set via config.toml or command line, 
    but we can set the page layout and title here.
    """
    st.set_page_config(
        page_title="AI Bubble Watch",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Inject custom CSS for "Antigravity" look (Dark Mode enhancements)
    if theme == 'dark':
        st.markdown("""
            <style>
            /* General Dark Theme Enhancements */
            .stApp {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            /* Card Styling */
            .ag-card {
                background-color: #262730;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #464B5C;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                text-align: center;
                margin-bottom: 20px;
            }
            .ag-card-title {
                font-size: 1.2rem;
                color: #A3A8B8;
                margin-bottom: 10px;
            }
            .ag-card-value {
                font-size: 2.5rem;
                font-weight: bold;
                color: #4CAF50; /* Green for value */
            }
            </style>
        """, unsafe_allow_html=True)

def chart(data, title=None, x=None, y=None, type='line', height=400, hline=None, hline_color='red', hline_label=None):
    """
    Wrapper for plotting charts.
    """
    if data is None or data.empty:
        st.warning("No data available to plot.")
        return

    if type == 'line':
        if isinstance(data, pd.DataFrame):
            # If x and y are not provided, assume index is x and all columns are y
            if x is None:
                fig = px.line(data, title=title)
            else:
                fig = px.line(data, x=x, y=y, title=title)
        else:
            st.error("Data must be a pandas DataFrame.")
            return
    else:
        st.warning(f"Chart type '{type}' not implemented yet.")
        return

    # Add Horizontal Line if specified
    if hline is not None:
        fig.add_hline(y=hline, line_dash="dash", line_color=hline_color, annotation_text=hline_label)

    fig.update_layout(height=height)
    st.plotly_chart(fig, width='stretch')

def card(title, value, color=None):
    """
    Displays a metric card with custom styling.
    """
    color_style = f"color: {color};" if color else ""
    
    st.markdown(f"""
        <div class="ag-card">
            <div class="ag-card-title">{title}</div>
            <div class="ag-card-value" style="{color_style}">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def markdown(text, unsafe_allow_html=False):
    """
    Wrapper for st.markdown.
    """
    st.markdown(text, unsafe_allow_html=unsafe_allow_html)

def table(data, highlight_cols=None, highlight_func=None):
    """
    Wrapper for st.dataframe with optional styling.
    """
    if data is None or data.empty:
        st.info("No data to display.")
        return

    if highlight_cols and highlight_func:
        st.dataframe(data.style.map(highlight_func, subset=highlight_cols))
    else:
        st.dataframe(data)
