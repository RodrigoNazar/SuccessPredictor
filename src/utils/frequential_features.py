
import numpy as np


def downmixing(data):
    return np.sum(data, axis=1) / data.shape[1]


def spectral_centroid(xf, yf):

    sq_abs = np.abs(yf)**2

    den = np.sum(sq_abs)
    den = .0025 if den == 0.0 else den

    return np.sum(
        np.multiply(
            xf,
            sq_abs
        )
    ) / den


def spectral_slope(xf, yf):

    mag = np.abs(yf)

    mean_freq = np.mean(xf)
    mean_mag = np.mean(mag)

    numerator = np.sum(
        np.multiply(
            xf - mean_freq,
            mag - mean_mag
        )
    )

    denominator = np.sum(
        np.power(
            xf - mean_freq,
            2
        )
    )
    denominator = .0025 if denominator == 0.0 else denominator

    return numerator / denominator


def spectral_flux(yf_1, yf):
    return np.sqrt(
        np.sum(
            np.power(
                np.abs(yf) - np.abs(yf_1),
                2
            )
        )
    ) / yf.shape[0]


def spectral_flatness(xf, yf):
    numerator = np.exp(
        (1. / yf.shape[0]) * np.sum(
            np.log(np.abs(yf))
        )
    )

    denominator = (1. / yf.shape[0]) * np.sum(np.abs(yf))
    denominator = .0025 if denominator == 0.0 else denominator

    return numerator / denominator


if __name__ == '__main__':
    mod = '''
    Módulo de útiles para el taller
    '''
    print(mod)
