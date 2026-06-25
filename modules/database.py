import sqlite3
import pandas as pd
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "financial_data.db")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Revenue REAL,
            Expenses REAL,
            Marketing_Expense REAL,
            Salary_Expense REAL,
            Operational_Expense REAL,
            Profit REAL,
            Region TEXT
        )
    ''')
    conn.commit()
    conn.close()
def save_dataframe_to_db(df):
    """Saves or appends clean DataFrame records into SQLite with column filtering."""
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Sabhi columns ke extra spaces hatayein (Agar Excel se blank space aa gayi ho)
    df.columns = df.columns.str.strip()
    
    # 2. Database schema ke hisaab se columns ko rename karein
    clean_df = df.rename(columns={
        'Marketing Expense': 'Marketing_Expense',
        'Salary Expense': 'Salary_Expense',
        'Operational Expense': 'Operational_Expense'
    })
    
    # 3. Sirf wahi columns select karein jo SQL database schema mein hain
    # Isse agar Excel mein koi extra blank column hoga toh woh automatic delete ho jayega
    allowed_columns = [
        'Date', 'Revenue', 'Expenses', 'Marketing_Expense', 
        'Salary_Expense', 'Operational_Expense', 'Profit', 'Region'
    ]
    
    # Sirf allowed columns ko filter kar ke nikaalein
    final_df = clean_df[[col for col in allowed_columns if col in clean_df.columns]]
    
    # 4. Database mein insert karein
    final_df.to_sql("financial_records", conn, if_exists="append", index=False)
    conn.close()
