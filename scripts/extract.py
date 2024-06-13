import requests
import pandas as pd
import os

def extract():
    # Define the API endpoint
    api_url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
    
    # Fetch data from the API
    response = requests.get(api_url)
    data = response.json()
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data['hits']['hits'])
    
    # Normalize the JSON data to flatten nested structures
    df = pd.json_normalize(df['_source'])
    
    # Define the file path
    directory = 'data'
    file_path = os.path.join(directory, 'consumer_complaints_raw.csv')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Save the raw data to a CSV file
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    extract()
