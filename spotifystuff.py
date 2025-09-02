import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="0bd2902b55614260ae224e84938827a5",
        client_secret="bcbf52651e6d4353b2364a0fc84e0da7",
        redirect_uri="http://127.0.0.1:8080",
        scope="user-library-read",
    )
)

# Example: search for a track
results = sp.search(q="Nujabes", limit=5, type="track")

for idx, track in enumerate(results["tracks"]["items"]):
    print(f"{idx+1}. {track['name']} by {track['artists'][0]['name']}")
