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
    conn = sqlite3.connect(DB_PATH)
    clean_df = df.rename(columns={
        'Marketing Expense': 'Marketing_Expense',
        'Salary Expense': 'Salary_Expense',
        'Operational Expense': 'Operational_Expense'
    })
    clean_df.to_sql("financial_records", conn, if_exists="append", index=False)
    conn.close()

def load_data_from_db():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM financial_records", conn)
        if not df.empty:
            df = df.rename(columns={
                'Marketing_Expense': 'Marketing Expense',
                'Salary_Expense': 'Salary Expense',
                'Operational_Expense': 'Operational Expense'
            })
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()

def clear_database():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM financial_records")
        conn.commit()
        conn.close()
