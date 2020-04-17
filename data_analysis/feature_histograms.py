import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

features = ['Popularity']
data_file = "../data/full_dataset.csv"
big_frame = pd.read_csv(data_file, index_col=False)
big_frame = big_frame.astype({'Success': int})
print(big_frame.info())

success = big_frame[big_frame['Success'] == 1]

not_success = big_frame[big_frame['Success']==0]

colors = ['green', 'red']
for feat in features:
	plt.hist([success[feat], not_success[feat]], 20, density=True, histtype='bar', color=colors, label=['Success', 'Not Sucess'])
	#plt.hist([survived_predict, died_predict], 20, stacked=True, histtype='step', color=colors, label=['survived', 'died'])
	plt.title(feat)
	plt.legend(prop={'size': 10})
	plt.show()
