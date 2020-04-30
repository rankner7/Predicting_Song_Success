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

def fix_date(date):
    return int(date[:4])

# fix the data column

big_frame['date_year'] = big_frame['Date'].apply(fix_date)

success = big_frame[(big_frame['Success'] == 1) & (big_frame['date_year'] > 2005)]

#not_success = big_frame[big_frame['Success']==0]

colors = ['green', 'red']

for feat in features:
    # Fit with polyfit
    x = success['date_year']
    y = success[feat],
    plt.scatter(x, y , color = 'blue'),
	m, b = np.polyfit(success['date_year'], success[feat], 1)
    plt.plot(x, m * x + b, color = 'green')
    #plt.hist([success[feat], not_success[feat]], 20, density=True, histtype='bar', color=colors, label=['Success', 'Not Sucess'])
    # #plt.hist([survived_predict, died_predict], 20, stacked=True, histtype='step', color=colors, label=['survived', 'died'])
    plt.title(feat)
    plt.show()


