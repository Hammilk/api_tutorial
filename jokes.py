import requests

url = "https://catfact.ninja/fact"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data["fact"])  # key is "fact" here, not "text"
else:
    print("Error:", response.status_code)
