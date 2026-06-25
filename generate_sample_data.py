import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data():
    np.random.seed(42)
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i*30) for i in range(24)]
    
    regions = ['North', 'South', 'East', 'West']
    data = []
    
    for dt in dates:
        for reg in regions:
            base_rev = np.random.randint(40000, 80000) if dt.month not in [11, 12] else np.random.randint(80000, 120000)
            marketing = np.random.randint(5000, 15000)
            salary = np.random.randint(15000, 25000)
            operational = np.random.randint(10000, 20000)
            
            expenses = marketing + salary + operational
            revenue = base_rev
            profit = revenue - expenses
            
            data.append({
                "Date": dt.strftime("%Y-%m-%d"),
                "Revenue": revenue,
                "Expenses": expenses,
                "Marketing Expense": marketing,
                "Salary Expense": salary,
                "Operational Expense": operational,
                "Profit": profit,
                "Region": reg
            })
            
    df = pd.DataFrame(data)
    df.to_csv("sample_financial_data.csv", index=False)
    print("✓ 'sample_financial_data.csv' created successfully!")

if __name__ == "__main__":
    generate_data()
