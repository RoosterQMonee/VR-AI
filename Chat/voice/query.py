import requests

def query(API_URL, headers, payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
