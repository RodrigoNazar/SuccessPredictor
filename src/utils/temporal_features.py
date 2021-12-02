
import numpy as np


def downmixing(data):
    # Obtiene el proceso de downmixing de una señal de n canales
    return np.sum(data, axis=1) / data.shape[1]


def centroid(data):
    # Obtiene el centroide de la señal
    data = np.absolute(data)

    den = .0025 if np.sum(data, axis=0) == 0.0 else np.sum(data, axis=0)

    return np.sum(
        np.multiply(
            np.array([i for i in range(data.shape[0])]),
            data
        )
    ) / den


def mean(data):
    # Obtiene el promedio de la señal
    return np.sum(data, axis=0) / data.shape[0]


def var(data, biased=False):
    # Obtiene la varianza de la señal
    den = data.shape[0] - 1 if biased else data.shape[0]
    aux = data - mean(data)

    return np.sum(
        np.power(
            aux,
            2
        )
    ) / den


def skewness(data):
    # Obtiene la skewness de la señal
    den = (var(data) ** 3/2) * data.shape[0]
    den = 0.0025 if den == 0.0 else den

    aux = data - mean(data)
    return np.clip(
        np.sum(
            np.power(
                aux,
                3
            )
        ) / den,
        -5e3, 5e3)
    # Tuve que agregar la función clip,
    # porque estaba obteniendo peaks muy grandes


def kurtosis(data):
    # Obtiene la kurtosis de la señal
    den = (var(data) ** 4/2) * data.shape[0]
    den = .0025 if den == 0.0 else den

    aux = data - mean(data)
    return np.clip(
        np.sum(
            np.power(
                aux,
                4
            )
        ) / den - 3,
        -10e5, 10e5)
    # Tuve que agregar la función clip,
    # porque estaba obteniendo peaks muy grandes


def RMS(data):
    return np.sqrt(
        np.sum(
            np.power(
                data,
                2
            )
        ) / data.shape[0]
    )


def max_amplitude(data):
    # Obtiene el valor máximo de amplitud
    return np.max(
        np.absolute(
            data
        )
    )


def zcr(data):
    # Obtiene el número de cruces por cero de la señal
    n_samples = data.shape[0]

    count = 0

    for i in range(n_samples):
        if i != n_samples - 1:
            if data[i] == 0 and data[i+1] < 0:
                count += 1
            elif data[i] == 0 and data[i+1] > 0:
                count += 1
            elif data[i] > 0 and data[i+1] < 0:
                count += 2
            elif data[i] < 0 and data[i+1] > 0:
                count += 2

    return count / (2 * n_samples)
