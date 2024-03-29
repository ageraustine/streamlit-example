import requests
import os

API_URL = os.environ["API_URL"]
def query(payload, headers):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
