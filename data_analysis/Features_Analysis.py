import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit

features = [
	'Duration',
	'acousticness',
	'danceability',
	'energy',
	'instrumentalness',
	'key',
	'liveness',
	'loudness',
	'mode',
	'speechiness',
	'tempo',
	'time_signature',
	'valence'
]

data_file = "../data/full_dataset_0.csv"
big_frame = pd.read_csv(data_file, index_col=False)
big_frame = big_frame.astype({'Success': int})
print(big_frame.info())

num_colums = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numerical_columns = list(big_frame.select_dtypes(include=num_colums).columns)
big_frame = big_frame[numerical_columns]

correlation_matrix = big_frame.corr()
correlation_factor = 0.5
correlated_features = set()
for i in range(len(correlation_matrix .columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > correlation_factor:
            colname = correlation_matrix.columns[i]
            correlated_features.add(colname)

print('{} Highly correlated columns : {}'.format( correlation_factor, correlated_features ))
def fix_date(date):
    return int(date[:4])
