import pandas as pd
from sqlalchemy import create_engine
import mysql

def load():
    # Replace the following variables with your own values
    username = 'admin'
    password = 'Billions+focus26'
    host = 'database-1.ctmm8csywzxg.us-east-1.rds.amazonaws.com'
    port = '3306'  # Default MySQL port
    database = 'database-1'
    
    # Database connection string
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
    
    # Define the directory where your data is located
    data_directory = r'C:\Users\LENOVO\OneDrive - Texas State University\Desktop\etl_complete\data'
    
    # Load the raw data
    df = pd.read_csv(f'{data_directory}\\consumer_complaints_raw.csv')
    df.to_sql('consumer_complaints_raw', con=engine, if_exists='replace', index=False)
    
    # Load the transformed data
    complaints_by_product = pd.read_csv(f'{data_directory}\\complaints_by_product.csv')
    complaints_by_state = pd.read_csv(f'{data_directory}\\complaints_by_state.csv')
    complaints_by_company = pd.read_csv(f'{data_directory}\\complaints_by_company.csv')
    
    complaints_by_product.to_sql('complaints_by_product', con=engine, if_exists='replace', index=False)
    complaints_by_state.to_sql('complaints_by_state', con=engine, if_exists='replace', index=False)
    complaints_by_company.to_sql('complaints_by_company', con=engine, if_exists='replace', index=False)

if __name__ == "__main__":
    load()
