import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import spotipy
import ticketpy
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

ticketmaster_api = os.environ["TICKETMASTER_API_KEY"]


# --- Spotify ---
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://127.0.0.1:8080",
        scope="user-library-read user-top-read",
    )
)

top_tracks = sp.current_user_top_artists(limit=20)
top_artists = [item["name"] for item in top_tracks["items"]]
# only for testing purposes
top_artists.append("Story So Far")
print(top_artists)

# --- Ticketmaster ---
tm_client = ticketpy.ApiClient(ticketmaster_api)


def ticket(artist):
    now_ct = datetime.now(ZoneInfo("America/Chicago"))
    plus1_ct = now_ct + relativedelta(months=1)
    start_z = now_ct.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_z = plus1_ct.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")

    # simple retry w/ backoff for 429s
    backoff = 0.5  # start at 500ms
    for attempt in range(5):
        try:
            resp = tm_client.events.find(
                keyword=artist,
                country_code="US",
                state_code="MO",
                start_date_time=start_z,
                end_date_time=end_z,
                sort="date,asc",
                size=50,
            )
            break  # success -> exit retry loop
        except Exception as e:
            msg = str(e)
            if "429" in msg or "Spike arrest" in msg or "rate" in msg.lower():
                time.sleep(backoff)
                backoff = min(backoff * 2, 8)  # exponential backoff, cap at 8s
                continue
            raise  # other errors: bubble up

    # iterate pages -> events
    for page in resp:
        for ev in page:
            name = ev.name
            # choose a date
            when = getattr(getattr(ev, "dates", None), "start", None)
            dt_iso = getattr(when, "dateTime", None) if when else None
            if dt_iso:
                dt_ct = datetime.fromisoformat(
                    dt_iso.replace("Z", "+00:00")
                ).astimezone(ZoneInfo("America/Chicago"))
                when_str = dt_ct.strftime("%Y-%m-%d %H:%M")
            else:
                # fallback to localDate if time is TBA
                when_str = getattr(when, "localDate", "TBA") if when else "TBA"

            v = ev.venues[0] if getattr(ev, "venues", None) else None
            if v:
                city = getattr(getattr(v, "city", None), "name", None)
                state = getattr(
                    getattr(v, "state", None), "stateCode", None
                ) or getattr(getattr(v, "state", None), "name", None)
                country = getattr(getattr(v, "country", None), "countryCode", None)
                venue_str = f"{v.name}" + (
                    f" — {', '.join(x for x in (city, state, country) if x)}"
                    if city or state or country
                    else ""
                )
            else:
                venue_str = "Unknown venue"

            print(f"{when_str} — {name} @ {venue_str}")


# walk artists with a small delay to avoid spike arrest (≤5 req/sec, no bursts)
for artist in top_artists:
    ticket(artist)
    time.sleep(0.25)  # 250ms between calls (~4 req/sec, burst-safe)
