
import cv2
import json
import os
import csv

from scipy.fft import fft
import numpy as np

from utils.wavfile import read
from utils.spotipy_utils import fetch_playlist



unwanted_files = ['.DS_Store']

def SplitAndProcessData(data, features=[], debug=False):
    '''
    Input:
        data: list
    Output:
        X_train
        labels_train
    '''
    X_train = []
    labels_train = []

    for elem in data:

        elem = np.array(elem)

        feature_train = []

        # temporal features
        feature_train = [feature(elem) for feature in features
                         if 'spectral' not in feature.__name__
                         # and 'mfcc' not in feature.__name__
                         ]

        # Freq features
        samplerate = 44100
        N = elem.shape[0]

        T = 1.0 / samplerate

        yf = fft(elem)[1:N//2]

        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

        if xf.shape[0] - yf.shape[0] > 0:
            # Padding just in case the samples arent equal length
            yf = np.pad(yf, (xf.shape[0] - yf.shape[0], 0), 'edge')

        feature_train += [feature(xf, yf) for feature in features
                          if 'spectral' in feature.__name__]

        # if 'mfcc' in [feature.__name__ for feature in features]:
        #     # MFCC features
        #     mfcc_features = [feature(elem, samplerate=samplerate,
        #                              nfft=512)
        #                      for feature in features
        #                      if 'mfcc' in feature.__name__][0]
        #
        #     mfcc_features = mfcc_features.sum(axis=0).tolist()
        #
        #     feature_train += mfcc_features

        # Process the data
        X_train.append(feature_train)

    if debug:
        print('X_train', len(X_train), type(X_train))
        print('labels_train', len(labels_train), labels_train[0])

    return np.nan_to_num(np.array(X_train)).astype(np.float),


def LoadData(data_path, playlists_id, unwanted_files=unwanted_files):
    '''
    Estructura de data:
    data = {
        'train': {
            'clase0': [
                {
                    'name': file,
                    'data': read(f'{data_path}/{elem}/{file}')[:2],
                },
                {
                    'name': file,
                    'data': read(f'{data_path}/{elem}/{file}')[:2],
                }
            ],
            'clase1': [

            ],
            .
            .
            .
        },
        'test': [...]
    }
    '''

    print('\n\t\t > OBTENIENDO LA INFORMACIÓN DE SPOTIFY <')
    data = {
        'train': fetch_playlist(playlists_id)
    }

    print(data)

    return data


def getThresholdImgs(img):
    '''
    Compute the threshold image of the three canals
    :params:
    img

    :returns:
    th_R, th_G, th_B
    '''

    img_R, img_G, img_B = cv2.split(img)

    _, th_R = cv2.threshold(img_R, 127, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _, th_G = cv2.threshold(img_G, 127, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _, th_B = cv2.threshold(img_B, 127, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return th_R, th_G, th_B


def printImg(img, factor, time):
    '''
    Prints an image and resize it by the factor
    '''
    if len(img.shape) == 2:
        x, y = img.shape
    elif len(img.shape) == 3:
        x, y, _ = img.shape

    if factor != 0:
        x = int(x/factor)
        y = int(y/factor)

    imgr = cv2.resize(img, (y, x))

    cv2.imshow('Training_01', imgr)
    cv2.waitKey(time)
    cv2.destroyAllWindows()


def isInside(out1, out2, in1, in2):

    x = out1[0] < in1[0] < in2[0] < out2[0]
    y = out1[1] < in1[1] < in2[1] < out2[1]
    return x and y


def segmentate(img):
    mser = cv2.MSER_create()

    regions, rects = mser.detectRegions(img)

    if isinstance(rects, list):
        rects = [i for i in rects
                 if (i[0] != 1 and i[1] != 1) and (i[0] != 0 and i[1] != 0)]
    else:
        rects = [i for i in rects.tolist()
                 if (i[0] != 1 and i[1] != 1) and (i[0] != 0 and i[1] != 0)]

    insideRects = []

    # Filters rects that are inside of others
    for (x1, y1, w1, h1) in rects:
        for (x2, y2, w2, h2) in rects:
            if isInside((x1, y1), (x1+w1, y1+h1), (x2, y2), (x2+w2, y2+h2)):
                insideRects.append([x2, y2, w2, h2])

    return [i for i in rects if i not in insideRects]


def extractSubmatrix(matrix, upperPoint, downerPoint):
    return np.array([x[upperPoint[0]:downerPoint[0]]
                    for x in matrix[upperPoint[1]:downerPoint[1]]])


def saveJson(name, data):
    with open('data/' + name + '.json', 'w') as file:
        file.write(json.dumps(data, indent=2))

def saveFeatures(name, X_train, labels_train, features=[], debug=True):

    X_train = np.array(X_train)

    print(type(features))

    labels_train = labels_train.tolist() + [feature.__name__ for feature in features]

    labels_train = np.array(labels_train.copy())

    print(labels_train)

    print(X_train.shape)
    print(labels_train.shape)

    data = np.column_stack((labels_train, X_train)).T.tolist()

    with open('features/csv/' + name + '.csv', 'w') as file:
        writer = csv.writer(file)

        # Escribe las features y header
        writer.writerows(data)

    if debug:
        print('Features actualizadas!')
        print('labels_train.shape', 'X_train.shape')
        print(labels_train.shape, X_train.shape)
