
import json
import datetime

from pybalu.feature_selection import clean
from pybalu.feature_transformation import normalize
import matplotlib.pyplot as plt
from python_speech_features import mfcc
import numpy as np

import utils.classifier_strategies as c
from utils.utils import LoadData, SplitAndProcessData, saveFeatures

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
FEATURES_METHODS = [FEATUES[i] for i in FEATURES_NAMES][:-1]

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

'''
Rutina principal del Algoritmo de procesamiento
'''
def main(data_path=DATA_PATH, playlists_id=PLAYLISTS_ID,
         features=FEATURES_METHODS, debug=DEBUG):

    start = datetime.datetime.now()

    print('\nLas features a extraer:',
          [i.__name__ for i in features])

    data = fetch_playlist(playlists_id[1], debug=debug)[:50]
    data = process_spotify_data(data, debug=debug)

    data_train_spotify, songs_train = spotify_data_matrix(data, debug=debug)

    data_train = fetch_track_data(data_train_spotify, playlists_id[5], debug)

    data_train = parse_track_data(data_train, playlists_id[5], debug)

    data_train = SplitAndProcessData(data_train, features=features)
    data_train = np.array(data_train)[0, :, :]

    data = np.column_stack((data_train_spotify.copy(), data_train.copy())).T.tolist()

    # Guardamos los datos de las features
    saveFeatures('features_2010', data, songs_train, features=features)

    print('\n\t> Tiempo de ejecucion del algoritmo: ', (datetime.datetime.now() - start))



if __name__ == '__main__':
    main()
