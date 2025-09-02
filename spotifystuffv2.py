import requests

CLIENT_ID = "filler"
CLIENT_SECRET = "filler"

URL = "https://accounts.spotify.com/api/token"
# connect
auth_response = requests.post(
    URL, data={"grant_type": "client_credentials"}, auth=(CLIENT_ID, CLIENT_SECRET)
)
access_token = auth_response.json()["access_token"]

# find track
headers = {"Authorization": f"Bearer {access_token}"}
params = {"q": "Nujabes", "type": "track", "limit": 5}

resp = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

# 3. Print results
for item in resp.json()["tracks"]["items"]:
    print(f"{item['name']} by {item['artists'][0]['name']}")
