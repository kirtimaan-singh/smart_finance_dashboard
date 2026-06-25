import plotly.express as px
import pandas as pd

def plot_revenue_trend(df):
    df_sorted = df.copy()
    df_sorted['Date'] = pd.to_datetime(df_sorted['Date'])
    monthly = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))[['Revenue', 'Profit']].sum().reset_index()
    monthly['Date'] = monthly['Date'].astype(str)
    
    fig = px.line(monthly, x='Date', y=['Revenue', 'Profit'], 
                  labels={'value': 'Amount ($)', 'Date': 'Timeline'},
                  title='Revenue & Net Profit Chronological Trend',
                  template='plotly_dark', color_discrete_sequence=['#00D2FF', '#00FF87'])
    return fig

def plot_expense_breakdown(df):
    m_exp = df['Marketing Expense'].sum()
    s_exp = df['Salary Expense'].sum()
    o_exp = df['Operational Expense'].sum()
    
    fig = px.pie(names=['Marketing', 'Salary', 'Operational'], values=[m_exp, s_exp, o_exp], 
                 title='Structural Expense Allocations', template='plotly_dark')
    return fig

def plot_regional_performance(df):
    regional = df.groupby('Region')['Revenue'].sum().reset_index()
    fig = px.bar(regional, x='Region', y='Revenue', title='Gross Revenue Capture by Region',
                 template='plotly_dark', color='Revenue')
    return fig
