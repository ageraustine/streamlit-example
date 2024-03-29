import requests

def query(payload, headers):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
