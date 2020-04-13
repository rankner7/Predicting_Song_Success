import argparse
import logging
import os

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

print(CLIENT_ID)
print(CLIENT_SECRET)
scope = 'playlist-modify-public'

track_id = '2NfDvle0RwbbPmRVtUuIuX'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(), scope='playlist-read-private,')
username = 'ronnieankner'
playlist = 'banginClassicals'
sp.trace=False
results = sp.current_user_playlists(limit=50)
for i, item in enumerate(results['items']):
	print("%d %s" % (i, item['name']))
#sp.user_playlist_add_tracks(username, playlist, track_id)
#res = sp.track(track_id)
#print(res)


