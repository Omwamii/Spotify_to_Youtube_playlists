#!/usr/bin env python

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
print(results)
