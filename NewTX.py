import requests

url = "http://127.0.0.1:5000/transactions/new"
payload = {
    "sender": "address1",
    "recipient": "address2",
    "amount": 10
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
