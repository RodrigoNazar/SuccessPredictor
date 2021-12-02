import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

SPOTIPY_CLIENT_ID = '1bd287021f34474799d1e87d14bd77b8'
SPOTIPY_CLIENT_SECRET = 'ad02f5ddb016462f915637070a3b89df'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    scope=scope
))

'''
results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])


playlists = sp.user_playlists('matiasaravena1')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

results = sp.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

'''

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
