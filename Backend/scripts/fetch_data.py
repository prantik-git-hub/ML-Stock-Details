import requests
import pandas as pd
from config import API_KEY, BASE_URL
from scripts.db_utils import insert_raw_data

def fetch_financial_data(company_id):
    url = f"{BASE_URL}?id={company_id}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        insert_raw_data(company_id, data)
        return data
    else:
        print(f"Failed for {company_id}")
        return None

def fetch_all():
    df = pd.read_excel("nifty100companies.xlsx")
    for company_id in df['CompanyID']:
        fetch_financial_data(company_id)

if __name__ == "__main__":
    fetch_all()