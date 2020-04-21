## Song Data Folder
# Full_DataSet Variants
* full_dataset_0 through full_dataset_3 contain about **1.8 MILLION** Songs worth of data spanning from 1946-2019
* data is stored as a pandas DataFrame converted to csv
  * file _full_dataset_0.csv_ contains the header for the data set and can be read in with:
```python
import pandas as pd
pd.read_csv(file_name, index_col=False, low_memory=False)
```
  * subsequent _full_dataset_X.csv_ are continuations of the dataset and **_do not contain the headers_**. Therefore they should be read in with:
```python
pd.read_csv(fil_name, index_col=False, low_memory=False, header=None)
```
  * once all datasets are read, the full dataset can be created by adding the proper column headers from the Dataframe acquired from reading in _full_dataset_0.csv_ to the DataFrames acquired from the other files and concatenating them with **pd.concat()**
* The Data Set contains the following information compiled from spotify:
  * Song Title
  * Artist(s)
  * Date
  * Spotify ID
  * Popularity - metric calculated by spotify from total listens and 'recent-ness' of listens (0 is low, 100 is max)
  * Duration (ms)
  * Danceability
  * Energy
  * Key
  * Loudness
  * Mode
  * Speechiness
  * Acoustiness
  * Instrumentalness
  * Liveness
  * Valence
  * Tempo
  * Time Signature
  * Success
* Further Description of the features can be found at: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
* The Success column is a custom metric which indicates if a song is a hit or not
  * A hit was determined if it was found on the top billboard list from 1946-2019, which is a compiled list of the top 100 billboard hits from each year
  * There are approximately 5800 hits in the data set
  * Popularity can also potentially be employed as a success metric, but the main goal of this investigation is compare billboard vs not billboard
  * Yes, billboard can be a little biased and not specifically fit your taste. For example, Madonna has the most billboard hits, trumping even Queen and Frank Sinatra :/

# 'List_' Files
These files contain the raw information pulled from the internet about songs, artists, or both. Formatting is not consistent, so you need to investigate the files yourself, but across all files, data entries are separated by '\n' so that's a good first place to start
