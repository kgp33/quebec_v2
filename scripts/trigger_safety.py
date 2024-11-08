#this is just a file to trigger a safety scan

import requests

def fetch_data():
    url = 'https://example.com'
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")

if __name__ == "__main__":
    fetch_data()