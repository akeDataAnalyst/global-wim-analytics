import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Global WIM Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS
st.markdown("""
    <style>
        /* Global dark background */
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117 !important;
            color: #e0e0e0 !important;
        }
        .stApp {
            background-color: #0e1117;
        }
        
        /* Text & headings */
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #f0f4f8 !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d;
        }
        .sidebar .sidebar-content {
            background-color: #161b22;
        }
        
        /* Metrics cards */
        .stMetric {
            background-color: #1f2937 !important;
            border: 1px solid #374151;
            border-radius: 8px;
            padding: 1rem;
            color: #e5e7eb !important;
        }
        .stMetric label {
            color: #9ca3af !important;
        }
        .stMetric .stMetric-value {
            color: #60a5fa !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1f2937 !important;
            border-radius: 8px 8px 0 0;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #2d3748 !important;
            color: #d1d5db !important;
            border-radius: 6px 6px 0 0;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #374151 !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #3b82f6 !important;
            color: white !important;
        }
        
        /* Expander */
        .stExpander {
            background-color: #1f2937 !important;
            border: 1px solid #374151;
            color: #e5e7eb;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #3b82f6 !important;
            color: white !important;
            border: none;
        }
        .stButton > button:hover {
            background-color: #2563eb !important;
        }
        
        /* File uploader */
        .stFileUploader label {
            color: #d1d5db !important;
        }
        
        /* Footer */
        .footer-text {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #0e1117;
            text-align: center;
            padding: 12px;
            font-size: 0.85rem;
            color: #9ca3af;
            border-top: 1px solid #30363d;
            z-index: 999;
        }
    </style>
""", unsafe_allow_html=True)

# Title & Introduction
st.title("Global Warehousing & Inventory Dashboard")

# Load Data
@st.cache_data(show_spinner="Loading data...")
def load_data():
    try:
        df_full = pd.read_csv('analytics_ready_inventory.csv')
        df_country = pd.read_csv('kpi_by_country.csv')
        
        for col in ['last_received_date', 'last_distributed_date', 'expiry_date']:
            if col in df_full.columns:
                df_full[col] = pd.to_datetime(df_full[col], errors='coerce')
        
        with open('global_kpis.json', 'r', encoding='utf-8') as f:
            global_kpis = json.load(f)
        
        return df_full, df_country, global_kpis
    
    except Exception as e:
        st.error(f"Data loading failed: {str(e)}")
        st.stop()

df, df_country, global_kpis = load_data()

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    
    countries = sorted(df['country'].unique())
    selected_countries = st.multiselect("Countries", options=countries, default=countries)
    
    item_types = sorted(df['item_type'].unique())
    selected_items = st.multiselect("Item Types", options=item_types, default=item_types)
    
    min_risk, max_risk = int(df['risk_score'].min()), int(df['risk_score'].max())
    risk_threshold = st.slider("Min Risk Score", min_risk, max_risk, min_risk, step=5)
    
    if st.button("Reset Filters"):
        st.rerun()

# Apply filters
filtered_df = df[
    (df['country'].isin(selected_countries)) &
    (df['item_type'].isin(selected_items)) &
    (df['risk_score'] >= risk_threshold)
]

# KPI Cards
st.subheader("Key Performance Indicators")

cols = st.columns(4)
with cols[0]:
    st.metric("Total Stock", f"{filtered_df['stock_level_current'].sum():,}")
with cols[1]:
    st.metric("% Expired", f"{filtered_df['is_expired'].mean()*100:.1f}%")
with cols[2]:
    st.metric("Avg Risk Score", f"{filtered_df['risk_score'].mean():.1f}")
with cols[3]:
    st.metric("% Stockout", f"{(filtered_df['stock_status'] == 'Stockout').mean()*100:.1f}%")

# Visualizations
st.subheader("Analytics")

tab1, tab2, tab3 = st.tabs(["Stock by Country", "Risk Distribution", "Expiry Urgency"])

with tab1:
    fig_stock = px.bar(
        filtered_df.groupby('country', as_index=False)['stock_level_current'].sum(),
        x='country', y='stock_level_current',
        title="Total Stock by Country",
        color='country',
        template="plotly_dark"
    )
    st.plotly_chart(fig_stock, use_container_width=True)

with tab2:
    fig_risk = px.box(
        filtered_df,
        x='country', y='risk_score',
        color='country',
        title="Risk Score Distribution by Country",
        points='outliers',
        template="plotly_dark",
        hover_data=['item_type', 'stock_status', 'donor_compliance_status']
    )
    st.plotly_chart(fig_risk, use_container_width=True)

with tab3:
    urgency = filtered_df['expiry_urgency_tier'].value_counts().reset_index()
    urgency.columns = ['Tier', 'Count']
    fig_urgency = px.pie(
        urgency, values='Count', names='Tier',
        title="Expiry Urgency Distribution",
        hole=0.4,
        template="plotly_dark"
    )
    st.plotly_chart(fig_urgency, use_container_width=True)

# Upload & Export
with st.expander("📤 Upload & Report Export", expanded=False):
    tab1, tab2 = st.tabs(["Upload CSV", "Export Report"])

    with tab1:
        st.info("Expected columns: country, warehouse_id, item_code, stock_level_current, expiry_date, ...")
        uploaded_file = st.file_uploader("Upload new inventory CSV", type="csv")

        if uploaded_file:
            try:
                new_df = pd.read_csv(uploaded_file)
                st.success(f"Loaded {len(new_df)} rows")
                st.dataframe(new_df.head(10))
            except Exception as e:
                st.error(f"Error reading file: {e}")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Filtered Report", type="primary"):
                if filtered_df.empty:
                    st.warning("No data in current view")
                else:
                    csv = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "⬇️ Download Filtered Report",
                        csv,
                        f"WIM_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        "text/csv"
                    )
        with col2:
            if st.button("Download Full Dataset"):
                csv_full = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Download Full",
                    csv_full,
                    f"Full_WIM_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

# Footer
st.markdown(
    """
    <div class="footer-text">
        Global WIM Analytics Dashboard • 
        Built by Aklilu Abera • Inspired by humanitarian supply chain operations
    </div>
    """,
    unsafe_allow_html=True
)