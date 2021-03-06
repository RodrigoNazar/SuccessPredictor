
import json
import datetime

from pybalu.feature_selection import clean
from pybalu.feature_transformation import normalize
import matplotlib.pyplot as plt
from python_speech_features import mfcc
import numpy as np

import utils.classifier_strategies as c
from utils.utils import LoadData, SplitAndProcessData, saveFeatures, split_data
from utils.classifier_strategies import classifier_tests


from utils.spotipy_utils import (fetch_playlist,
                                 process_spotify_data,
                                 spotify_data_matrix,
                                 fetch_track_data,
                                 parse_track_data)

from utils.temporal_features import (centroid,
                                     mean,
                                     var,
                                     skewness,
                                     kurtosis,
                                     RMS,
                                     max_amplitude,
                                     zcr)


from utils.frequential_features import (spectral_centroid,
                                        spectral_slope,
                                        spectral_flatness)


FEATUES = {
    'centroid': centroid,
    'mean': mean,
    'var': var,
    'skewness': skewness,
    'kurtosis': kurtosis,
    'RMS': RMS,
    'max_amplitude': max_amplitude,
    'zcr': zcr,
    'spectral_centroid': spectral_centroid,
    'spectral_slope': spectral_slope,
    'spectral_flatness': spectral_flatness,
    'mfcc': mfcc
}


'''          ####        Hiperparametros del programa        ####
'''

# NO TOCAR
FEATURES_NAMES = ['centroid', 'mean', 'var', 'skewness', 'kurtosis', 'RMS',
                  'max_amplitude', 'zcr', 'spectral_centroid', 'spectral_slope',
                  'spectral_flatness', 'mfcc']


## PARAMETROS A CAMBIAR

# Features a utilizar
FEATURES_METHODS = [FEATUES[i] for i in FEATURES_NAMES]

# Despliegue de prints para debug
DEBUG = False

# Fuente de datos a utilizar
DATA_PATH = './data'

# ID's de las playlists a analizar
PLAYLISTS_ID = [
    '37i9dQZF1DX7Jl5KP2eZaS', # actuales
    '37i9dQZF1DX4o1oenSJRJd', # 2000
    '37i9dQZF1DXbTxeAdrVG2l', # 1990
    '37i9dQZF1DX4UtSsGT1Sbe', # 1980
    '37i9dQZF1DWTJ7xPn4vNaz', # 1970
    '37i9dQZF1DXc6IFF23C9jj'  # 2010
]

with open('./CREDENTIALS.txt', 'r') as f:
    credentials = f.read()
    credentials = json.loads(credentials)


'''
Rutina principal del Algoritmo de procesamiento
'''


def main(data_path=DATA_PATH, playlists_id=PLAYLISTS_ID,
         features=FEATURES_METHODS, debug=DEBUG):

    start = datetime.datetime.now()

    print('\nLas features a extraer:',
          [i.__name__ for i in features])

    data = fetch_playlist(playlists_id[1], debug=debug)[:50]
    ('data = fetch_playlist(playlists_id[1], debug=debug)[:50]')
    print(data)
    data = process_spotify_data(data, debug=debug)
    ('data = process_spotify_data(data, debug=debug)')
    print(data)

    songs_data_spotify, songs = spotify_data_matrix(data, debug=debug)
    ('songs_data_spotify, songs = spotify_data_matrix(data, debug=debug)')
    print(songs_data_spotify)

    songs_data = fetch_track_data(songs_data_spotify, playlists_id[5], debug)
    ('songs_data = fetch_track_data(songs_data_spotify, playlists_id[5], debug)')
    print(songs_data)

    songs_data = parse_track_data(songs_data, playlists_id[5], debug)
    ('songs_data = parse_track_data(songs_data, playlists_id[5], debug)')
    print(songs_data)

    songs_data = SplitAndProcessData(songs_data, features=features)
    ('songs_data = SplitAndProcessData(songs_data, features=features)')
    print(songs_data)

    sorted(songs_data, key=lambda song: song[0])
    ('sorted(songs_data, key=lambda song: song[0])')

    split_data(songs_data, .8, .1)
    ('split_data(songs_data, .8, .1)')

    data_train = np.array(songs_data)[0, :, :]
    ('data_train = np.array(songs_data)[0, :, :]')
    print(data_train)

    print(songs_data_spotify[:42].shape, data_train[:42].shape)
    ('print(songs_data_spotify[:42].shape, data_train[:42].shape)')
    print(print(songs_data_spotify[:42].shape, data_train[:42].shape))
    print(songs_data_spotify[:42].shape, data_train[:42].shape)
    print(songs_data_spotify[:42].shape, data_train[:42].shape)

    data = np.column_stack((songs_data_spotify[:42].copy(), data_train[:42].copy())).T.tolist()

    # Guardamos los datos de las features
    # saveFeatures('features_2010', data, songs, features=features)

    classifier_tests(
                    X_train=data_train,
                    labels_train=[str(i) for i in data_train],
                    X_test=data_train,
                    labels_test=[str(i) for i in data_train]
                )

    print('\n\t> Tiempo de ejecucion del algoritmo: ', (datetime.datetime.now() - start))



if __name__ == '__main__':
    main()
