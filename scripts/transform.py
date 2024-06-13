import pandas as pd
import os

def transform():
    # Define the directory path
    directory = r'C:\Users\LENOVO\OneDrive - Texas State University\Desktop\etl_complete\data'
    
    # Define the file paths
    input_file_path = os.path.join(directory, 'consumer_complaints_raw.csv')
    complaints_by_product_path = os.path.join(directory, 'complaints_by_product.csv')
    complaints_by_state_path = os.path.join(directory, 'complaints_by_state.csv')
    complaints_by_company_path = os.path.join(directory, 'complaints_by_company.csv')
    
    # Load the raw data from the CSV file
    df = pd.read_csv(input_file_path)
    
    # Transform data: Calculate the number of complaints per product
    complaints_by_product = df.groupby('product').size().reset_index(name='count')
    
    # Transform data: Calculate the number of complaints per state
    complaints_by_state = df.groupby('state').size().reset_index(name='count')
    
    # Transform data: Calculate the number of complaints per company
    complaints_by_company = df.groupby('company').size().reset_index(name='count')
    
    # Save the transformed data to CSV files
    complaints_by_product.to_csv(complaints_by_product_path, index=False)
    complaints_by_state.to_csv(complaints_by_state_path, index=False)
    complaints_by_company.to_csv(complaints_by_company_path, index=False)

if __name__ == "__main__":
    transform()
