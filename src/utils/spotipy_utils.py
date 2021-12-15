
import spotipy
import json
import random
import struct

import numpy as np

from urllib.request import urlopen
from spotipy.oauth2 import SpotifyOAuth


def fetch_playlist(playlists_id, credentials_path='./', debug=False):

    print('Obteniendo credenciales en fetch_playlist...')

    with open(credentials_path + 'CREDENTIALS.txt', 'r') as f:
        credentials = json.loads(f.read())

    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        credentials['SPOTIPY_CLIENT_ID'],
        credentials['SPOTIPY_CLIENT_SECRET'],
        credentials['SPOTIPY_REDIRECT_URI'],
        scope=scope
    ))

    print('\t> Credenciales aceptadas!')

    results = sp.playlist_items(playlists_id)

    data = []






    for z, i in enumerate(results['items']):
        '''album, artists, available_markets, disc_number, duration_ms, episode,
        explicit, external_ids, external_urls, href, id, is_local, name, popularity,
        preview_url, track, track_number, type, uri
        '''

        if debug:
            print(i['track'].keys())
            print(i['track']['name'])
            print(i['track']['href'])

            print(sp.audio_features(i['track']['href']))

            print(f'Canción número {z} procesada!')

        data.append(
            [z,
                {
                    'artists': i['track']['artists'],
                    'id': i['track']['id'],
                    'name': i['track']['name'],
                    'href': i['track']['href'],
                    'features': sp.audio_features(i['track']['id'])
                }
            ]
        )


    random.shuffle(data)

    return data

def process_spotify_data(data, debug=False):

    new_data = {
        'train': [],
    }

    for index, [ii, track] in enumerate(data):

        new_data['train'].append(
            {
                'id': track['id'],
                'name': track['name'],
                'artists': ' & '.join([i['name']
                                       for i in track['artists']]),
                'data':  [ii] + track['features'],
                'href': track['href']
            }
        )

    return new_data


def spotify_data_matrix(data, debug=False):

    data = data['train']

    data_labels = ['name', 'artists', 'href', 'z'] + \
                  list(data[0]['data'][1].keys())

    data_labels = np.array(['id'] + [
        i for i in data_labels if i not in ['type', 'id', 'track_href',
                                            'analysis_url', 'uri']
    ])

    data_elems = []

    for i in data:

        elem = [
                i['id'], i['name'], i['artists'], i['href']
            ] + [i['data'][0]] + [i['data'][1][j] for j in data_labels if j not in ['id', 'name', 'artists', 'href', 'z']]

        data_elems.append(elem)

    return np.array(data_elems), np.array(data_labels)


def fetch_track_data(data, playlists_id, debug, credentials_path='./', id_pos=0):

    print('Obteniendo credenciales en fetch_track_data...')

    with open(credentials_path + 'CREDENTIALS.txt', 'r') as f:
        credentials = json.loads(f.read())

    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        credentials['SPOTIPY_CLIENT_ID'],
        credentials['SPOTIPY_CLIENT_SECRET'],
        credentials['SPOTIPY_REDIRECT_URI'],
        scope=scope
    ))

    print('\t> Credenciales aceptadas!')

    results = sp.playlist_items(playlists_id)

    tracks_urls = data[:, id_pos]

    tracks_data = sp.tracks(tracks_urls)['tracks']

    data = []

    reviewed_tracks = []

    prev_reviewed_tracks_number = 100

    while len(data) <= 50:
        for track in tracks_data:
            try:
                with urlopen(track['preview_url']) as query:
                    if track['name'] not in reviewed_tracks:
                        data.append(query.read())
                        reviewed_tracks.append(track['name'])

            except Exception as e:
                if debug:
                    print('\ntrack', track)

                    print('\n', reviewed_tracks)
                    print(e)

        if len(data) == 50 or len(reviewed_tracks) == prev_reviewed_tracks_number:
            break

        prev_reviewed_tracks_number = len(reviewed_tracks)

    while len(data) < 50:
        data.append(data[-1])


    data = np.array(list(data))

    return data


def parse_track_data(data, playlists_id, debug=False, credentials_path='./', id_pos=0):
    '''
    Inspirado en:
    https://stackoverflow.com/questions/45688014/how-to-read-specific-bytes-from-a-binary-mp3-file-in-python
    '''

    new_data = []

    for entry in data:

        processed_entry = entry[0xA7:0xAC+1]
        processed_entry = struct.unpack("{}b".format(len(entry)), entry)

        new_data.append(processed_entry)

        if debug:
            print('process', len(processed_entry))
            print('type', type(processed_entry[0]))

    return np.array(new_data, dtype=object)
