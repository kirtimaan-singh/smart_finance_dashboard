import pandas as pd

def calculate_kpis(df):
    if df.empty:
        return 0, 0, 0, 0.0, 0.0
    
    total_revenue = df['Revenue'].sum()
    total_expenses = df['Expenses'].sum()
    net_profit = df['Profit'].sum()
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    df_sorted = df.copy()
    df_sorted['Date'] = pd.to_datetime(df_sorted['Date'])
    monthly_series = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))[['Revenue']].sum().reset_index()
    
    growth_rate = 0.0
    if len(monthly_series) > 1:
        prev_month = monthly_series.iloc[-2]['Revenue']
        curr_month = monthly_series.iloc[-1]['Revenue']
        if prev_month > 0:
            growth_rate = ((curr_month - prev_month) / prev_month) * 100
            
    return total_revenue, total_expenses, net_profit, profit_margin, growth_rate

def generate_insights_and_decisions(df):
    insights = []
    recommendations = []
    
    if df.empty:
        return ["No data available."], ["Upload data to begin."]
        
    df_sorted = df.copy()
    df_sorted['Date'] = pd.to_datetime(df_sorted['Date'])
    monthly = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))[['Revenue', 'Expenses', 'Profit', 'Marketing Expense']].sum().reset_index()
    
    if len(monthly) >= 2:
        curr = monthly.iloc[-1]
        prev = monthly.iloc[-2]
        
        exp_change = ((curr['Expenses'] - prev['Expenses']) / prev['Expenses']) * 100
        if exp_change > 10:
            insights.append(f"⚠️ Operational Expenses scaled rapidly by {exp_change:.1f}% month-over-month.")
            recommendations.append("• Audit operational cost spikes immediately. Implement stricter controls.")
            
        curr_margin = (curr['Profit'] / curr['Revenue']) * 100
        prev_margin = (prev['Profit'] / prev['Revenue']) * 100
        if curr_margin < prev_margin:
            insights.append(f"📉 Profit Margin weakened down to {curr_margin:.1f}% this month.")
            recommendations.append("• Renegotiate vendor pricing matrices or evaluate structural adjustments.")
    
    if not insights:
        insights.append("🟢 Operational flows show healthy consolidation.")
        recommendations.append("• Maintain current capital utilization footprint.")
        
    return insights, recommendations
