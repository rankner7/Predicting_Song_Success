import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import matplotlib.pyplot as plt

def split_train_and_test(full_dataset, percent_split):
    if not(percent_split > 0 and percent_split < 1):
        print("Invalid Split: Value must be between 0 and 1")
        return None

    data_points = full_dataset.shape[0]

    #Create Training_list
    training_list = sample(range(data_points), int(percent_split*data_points))
    training_list.sort()

    #Create Test List
    full = [x for x in range(0,data_points)]
    full_set = set(full)
    test_list = list(full_set - set(training_list))
    test_list.sort()

    training_set = full_dataset.iloc[training_list]
    test_set = full_dataset.iloc[test_list]

    training_set.reset_index(inplace=True, drop=True)
    test_set.reset_index(inplace=True, drop=True)

    if (training_set.shape[0] + test_set.shape[0]) == data_points:
        print("Good Split")
        return {'training_set':training_set, 'test_set': test_set}
    else:
        print("Whoops! BAD SPLIT. Not sure what happened :/")
        return None

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

data_file = "../data/full_dataset.csv"
big_frame = pd.read_csv(data_file, index_col=False)
big_frame = big_frame.astype({'Success': int})

successes = big_frame[big_frame['Success'] == 1]
fails = big_frame[big_frame['Success'] == 0]

success_IDs = successes['id'].tolist()

for i in range(0,1):
	analysis = sp.audio_analysis(success_IDs[i])
	segment_data = analysis['segments']
	print("%d Segments"%(len(segment_data)))
	pitches = []
	timbres = []
	for segment in segment_data:
		pitch_vec = segment['pitches']
		pitches.append(pitch_vec)
		timbre_vec = segment['timbre']
		timbres.append(timbre_vec)

	pitches = np.array(pitches)
	timbres = np.array(timbres)

	print("Pitch Shape: ", np.shape(pitches))
	print("  Datatype: ", type(pitches[0,0]))
	print("Timbre Shape: ", np.shape(timbres))
	print("  Datatype: ", type(timbres[0,0]))

rows = np.shape(pitches)[0]
cols = np.shape(pitches)[1]

segs = [x for x in range(0,rows)]

fig, (ax_pitch, ax_timbre) = plt.subplots(2)
for c in range(0, 2):
	ax_pitch.plot(segs, pitches[:,c])
	ax_timbre.plot(segs, timbres[:,c])

plt.tight_layout()
plt.show()

pitch_df = pd.DataFrame(pitches)
timbre_df = pd.DataFrame(timbres)

print(pitch_df.info())
print(timbre_df.info())





