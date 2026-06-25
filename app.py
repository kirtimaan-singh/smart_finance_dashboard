import streamlit as st
import pandas as pd
from io import BytesIO
from modules.database import init_db, save_dataframe_to_db, load_data_from_db, clear_database
from modules.auth import check_password, logout
from modules.analytics import calculate_kpis, generate_insights_and_decisions
from modules.visualizer import plot_revenue_trend, plot_expense_breakdown, plot_regional_performance

# Page configuration
st.set_page_config(page_title="Finto.ai | Premium Finance Analytics", page_icon="⚡", layout="wide")
init_db()

# --- HARDCORE PREMIUM UI OVERRIDES (CSS) ---
st.markdown("""
    <style>
    /* Main Background & Font tuning */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    }
    
    /* Neon Gradient Heading */
    .neon-title {
        font-size: 50px;
        font-weight: 800;
        background: linear-gradient(45deg, #00F2FE, #4FACFE, #00FF87);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 35px;
    }
    
    /* Glassmorphism KPI Cards */
    .glass-kpi {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-kpi:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 242, 254, 0.4);
    }
    
    /* Dynamic Metric Typography */
    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-val {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        font-family: 'Courier New', monospace;
    }
    
    /* Fancy Borders for Insights & Recommendations */
    .insight-box {
        background: rgba(239, 68, 68, 0.07);
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 4px 12px 12px 4px;
        color: #fca5a5;
    }
    .rec-box {
        background: rgba(16, 185, 129, 0.07);
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 4px 12px 12px 4px;
        color: #a7f3d0;
    }
    </style>
""", unsafe_allow_html=True)

if check_password():
    # Sidebar custom branding
    st.sidebar.markdown("<h2 style='text-align: center; color: #00F2FE; font-weight:800;'>⚡ Finto.ai</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='text-align: center; color: #64748b;'>Active Session: <b>{st.session_state['username']}</b></p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("⚡ NAVIGATE ENGINE", ["Executive Dashboard", "Data Pipeline Ingestion", "Control Center"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 Secure Terminate (Logout)", use_container_width=True):
        logout()

    raw_df = load_data_from_db()

    # --- 1. EXECUTIVE DASHBOARD ---
    if menu == "Executive Dashboard":
        st.markdown('<p class="neon-title">Finto.ai</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Next-Generation Next-Gen Financial Intelligence Terminal for SMBs</p>', unsafe_allow_html=True)
        
        if raw_df.empty:
            st.warning("⚡ Terminal lacks data registers. Please route to 'Data Pipeline Ingestion' to feed financial telemetry.")
        else:
            # Elegant minimalist filters
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                selected_region = st.selectbox("🌐 Market Territory", ["All Regions"] + list(raw_df['Region'].unique()))
            with f_col2:
                raw_df['Year'] = pd.to_datetime(raw_df['Date']).dt.year.astype(str)
                selected_year = st.selectbox("📅 Temporal Epoch (Year)", ["All Years"] + list(raw_df['Year'].unique()))
            
            # Filter processing
            filtered_df = raw_df.copy()
            if selected_region != "All Regions":
                filtered_df = filtered_df[filtered_df['Region'] == selected_region]
            if selected_year != "All Years":
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
                
            tot_rev, tot_exp, net_prof, prof_marg, growth = calculate_kpis(filtered_df)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Premium Glassmorphism Cards Grid
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.markdown(f"""
                    <div class="glass-kpi">
                        <div class="metric-label">🟢 Gross Revenue</div>
                        <div class="metric-val">${tot_rev:,.0f}</div>
                        <span style="color:#00FF87; font-size:12px; font-weight:600;">📈 MoM: {growth:+.1f}%</span>
                    </div>
                """, unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"""
                    <div class="glass-kpi">
                        <div class="metric-label">🔴 Total Outflows</div>
                        <div class="metric-val">${tot_exp:,.0f}</div>
                        <span style="color:#64748b; font-size:12px;">Burn Rate Active</span>
                    </div>
                """, unsafe_allow_html=True)
            with kpi_col3:
                st.markdown(f"""
                    <div class="glass-kpi">
                        <div class="metric-label">⚡ Net Retained Profit</div>
                        <div class="metric-val" style="color:#00F2FE;">${net_prof:,.0f}</div>
                        <span style="color:#64748b; font-size:12px;">Free Cash Flow</span>
                    </div>
                """, unsafe_allow_html=True)
            with kpi_col4:
                st.markdown(f"""
                    <div class="glass-kpi">
                        <div class="metric-label">💎 Net Margin</div>
                        <div class="metric-val" style="color:#00FF87;">{prof_marg:.1f}%</div>
                        <span style="color:#64748b; font-size:12px;">Capital Efficiency</span>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Charts Section
            v_col1, v_col2 = st.columns([2, 1])
            with v_col1:
                st.plotly_chart(plot_revenue_trend(filtered_df), use_container_width=True)
            with v_col2:
                st.plotly_chart(plot_expense_breakdown(filtered_df), use_container_width=True)
                
            st.plotly_chart(plot_regional_performance(filtered_df), use_container_width=True)
            
            st.markdown("---")
            
            # Heuristic Insights / Decision engine
            st.markdown("### 🧠 Heuristic Threat & Opportunity Diagnostic")
            insights, recommendations = generate_insights_and_decisions(filtered_df)
            
            inf_col1, inf_col2 = st.columns(2)
            with inf_col1:
                formatted_insights = "<br>".join([f"• {i}" for i in insights])
                st.markdown(f"""
                    <div class="insight-box">
                        <strong>⚠️ ANOMALIES & SIGNALS DETECTED:</strong><br><br>
                        {formatted_insights}
                    </div>
                """, unsafe_allow_html=True)
            with inf_col2:
                formatted_recs = "<br>".join([f"{r}" for r in recommendations])
                st.markdown(f"""
                    <div class="rec-box">
                        <strong>🎯 STRATEGIC DECISION PLAYBOOK:</strong><br><br>
                        {formatted_recs}
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            csv_buffer = BytesIO()
            filtered_df.to_csv(csv_buffer, index=False)
            st.download_button("📥 Extract Operational Ledger (CSV)", csv_buffer.getvalue(), "finto_ledger.csv", "text/csv")

    # --- 2. DATA PIPELINE INGESTION ---
    elif menu == "Data Pipeline Ingestion":
        st.markdown('<p class="neon-title">Data Pipeline</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Feed structured financial telemetry into Finto relational databases</p>', unsafe_allow_html=True)
        
        # AB ISME CSV AUR XLSX DONO ALLOWED HAIN!
        uploaded_file = st.file_uploader("Drop financial transaction sheets (.csv or .xlsx format)", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            # Agar file Excel hai toh excel parser chalega, nahi toh csv
            if uploaded_file.name.endswith('.xlsx'):
                uploaded_df = pd.read_excel(uploaded_file)
            else:
                uploaded_df = pd.read_csv(uploaded_file)
                
            st.markdown("### 📋 Telemetry Preview (Top 10 Records)")
            st.dataframe(uploaded_df.head(10), use_container_width=True)
            if st.button("🚀 Push to Central SQLite Cluster", use_container_width=True):
                save_dataframe_to_db(uploaded_df)
                st.balloons()
                st.success("Data successfully standard-indexed and structured in local DB registers!")
    # --- 3. CONTROL CENTER ---
    elif menu == "Control Center":
        st.markdown('<p class="neon-title">Control Center</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Administrative sandbox and cluster diagnostics</p>', unsafe_allow_html=True)
        st.error("🔒 CRITICAL AREA: Purging actions will wipe persistent tables completely.")
        
        if st.button("🚨 Wipe SQLite Storage Registers", use_container_width=True):
            clear_database()
            st.success("All local transactional database blocks zeroed-out successfully.")
