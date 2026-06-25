import streamlit as st
import pandas as pd
from io import BytesIO
from modules.database import init_db, save_dataframe_to_db, load_data_from_db, clear_database
from modules.auth import check_password, logout
from modules.analytics import calculate_kpis, generate_insights_and_decisions
from modules.visualizer import plot_revenue_trend, plot_expense_breakdown, plot_regional_performance

st.set_page_config(page_title="Smart Finance Analytics", page_icon="📈", layout="wide")
init_db()

st.markdown("""
    <style>
    .metric-card {
        background-color: #1F2635;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #00D2FF;
    }
    </style>
""", unsafe_allow_html=True)

if check_password():
    st.sidebar.markdown(f"<h3 style='color:#00D2FF;'>👤 Welcome, {st.session_state['username']}</h3>", unsafe_allow_html=True)
    menu = st.sidebar.radio("Navigation Menu", ["Dashboard Hub", "Data Ingestion Unit", "System Administration"])
    
    if st.sidebar.button("Logout"):
        logout()

    raw_df = load_data_from_db()

    if menu == "Dashboard Hub":
        st.title("📈 Smart Business Finance Analytics Dashboard")
        st.markdown("---")
        
        if raw_df.empty:
            st.warning("⚠️ No data in database. Please upload data via 'Data Ingestion Unit'.")
        else:
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                selected_region = st.selectbox("Filter Territory", ["All"] + list(raw_df['Region'].unique()))
            with col_f2:
                raw_df['Year'] = pd.to_datetime(raw_df['Date']).dt.year.astype(str)
                selected_year = st.selectbox("Filter Financial Year", ["All"] + list(raw_df['Year'].unique()))
            
            filtered_df = raw_df.copy()
            if selected_region != "All":
                filtered_df = filtered_df[filtered_df['Region'] == selected_region]
            if selected_year != "All":
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
                
            tot_rev, tot_exp, net_prof, prof_marg, growth = calculate_kpis(filtered_df)
            
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Total Revenue", f"${tot_rev:,.2f}", f"{growth:.2f}% MoM")
                st.markdown('</div>', unsafe_allow_html=True)
            with kpi_col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Total Expenses", f"${tot_exp:,.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with kpi_col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Net Profit", f"${net_prof:,.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with kpi_col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Profit Margin", f"{prof_marg:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
                
            st.markdown("---")
            
            v_col1, v_col2 = st.columns(2)
            with v_col1:
                st.plotly_chart(plot_revenue_trend(filtered_df), use_container_width=True)
            with v_col2:
                st.plotly_chart(plot_expense_breakdown(filtered_df), use_container_width=True)
                
            st.plotly_chart(plot_regional_performance(filtered_df), use_container_width=True)
            
            st.markdown("---")
            st.subheader("💡 Automated Insights & Decision Support")
            insights, recommendations = generate_insights_and_decisions(filtered_df)
            
            inf_col1, inf_col2 = st.columns(2)
            with inf_col1:
                st.info("📊 **Trends:**\n\n" + "\n".join(insights))
            with inf_col2:
                st.success("🎯 **Recommendations:**\n\n" + "\n".join(recommendations))
                
            csv_buffer = BytesIO()
            filtered_df.to_csv(csv_buffer, index=False)
            st.download_button("Download Report as CSV", csv_buffer.getvalue(), "report.csv", "text/csv")

    elif menu == "Data Ingestion Unit":
        st.title("📥 Operational Data Ingestion Framework")
        st.markdown("---")
        uploaded_file = st.file_uploader("Upload business sheets (.csv)", type=["csv"])
        
        if uploaded_file is not None:
            uploaded_df = pd.read_csv(uploaded_file)
            st.dataframe(uploaded_df.head(10), use_container_width=True)
            if st.button("Commit Records to SQLite Database"):
                save_dataframe_to_db(uploaded_df)
                st.success("🚀 Records successfully saved to Database!")

    elif menu == "System Administration":
        st.title("⚙️ System Control Management Console")
        st.markdown("---")
        if st.button("Wipe SQLite Database Records"):
            clear_database()
            st.success("🧹 Database cleared completely.")
