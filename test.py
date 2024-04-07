""" Module to test the basic usage of spotify functions
    uncomment the desired function you want to test from the if __name__ section
    run with 'python3 test.py
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

f_cl_id = open("sp_client_id", "r")
cl_id = f_cl_id.read()
f_cl_id.close()

# Read spotify client secret
f_cl_secret = open("sp_client_secret", "r")
cl_secret = f_cl_secret.read()
f_cl_secret.close()

os.environ['SPOTIPY_CLIENT_ID'] = cl_id
os.environ['SPOTIPY_CLIENT_SECRET'] = cl_secret
os.environ['SPOTIPY_REDIRECT_URI'] = "http://127.0.0.1:5000"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_playlist_names():
    playlists = sp.current_user_playlists().get('items')
    for playlist in playlists:
        print()
        print(playlist)
        print()
        # print(playlist.get('name'))
    return playlists

def get_playlists_info():
    playlists = sp.current_user_playlists().get('items')
    p_info = list()
    for playlist in playlists:
        image_url = playlist.get('images')[0].get('url') if playlist.get('images') else None
        data = {'id': playlist.get('id'), 'name': playlist.get('name'),
                'cover': image_url, 'tracks': playlist.get('tracks').get('total')}
        p_info.append(data)
    return p_info

def print_playlists_info():
    info = get_playlists_info()
    for item in info:
        print()
        print(item)
        print()

def get_playlist_tracks(playlist_id: str):
    playlist = sp.playlist(playlist_id)
    items = list()
    for item in playlist['tracks'].get('items'):
        items.append(item)
    return items

def print_playlists_tracks():
    playlists = get_playlists_info()
    for item in playlists:
        print()
        print(f"------- {item['name']} ---------")
        p_tracks = get_playlist_tracks(item['id'])
        print_track_names(p_tracks)
        print()

def print_track_names(playlist):
    for item in playlist:
        if item['track']:
            print(item['track']['name'])

if __name__ == "__main__":
    # print_playlists_info()
    # get_playlist_names()
    print_playlists_tracks()
