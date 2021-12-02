
import pandas as pd
import numpy as np
from scipy.linalg import svd

np.set_printoptions(threshold=5)
np.set_printoptions(precision=4)

data_path = 'features/csv/features_2010.csv'
data = pd.read_csv(data_path)

data["name"] = data["name"] + ' - ' + data["artists"]

data.drop('id', inplace=True, axis=1)
data.drop('name', inplace=True, axis=1)
data.drop('artists', inplace=True, axis=1)
data.drop('href', inplace=True, axis=1)

data = data.to_numpy().T

print('data nombre', data[0, :])
print('data', data[1:, :])
np.savetxt('features/txt/features_2010.txt', data[1:, :])
print(data.shape)
