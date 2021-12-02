import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    scope=scope
))

lz_uri = '37i9dQZF1DX7Jl5KP2eZaS'

results = sp.playlist_items(lz_uri)

for i in results['items']:
    '''album, artists, available_markets, disc_number, duration_ms, episode,
    explicit, external_ids, external_urls, href, id, is_local, name, popularity,
    preview_url, track, track_number, type, uri
    '''
    # print(i)
    for j in i['track']:
        print(i['track']['name'])
        print(i['track']['href'])

        print(sp.audio_features(i['track']['href']))



        # print(i['track']['track_number'])
        #     for w in j.keys():
        #         print(w)
        #         break
        break
    # break

# print(json.dumps([i['preview_url'] for i in results['tracks']], indent=2))
