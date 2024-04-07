from flask import Flask
from flask import render_template
from spo2yt import Spo2yt

app = Flask(__name__)

my_app = Spo2yt()

@app.route("/")
def index():
    for p in my_app.get_spotify_playlists():
        print(p['id'])
        track_info = my_app.get_spotify_playlist_tracks(p['id'])
        print()
        print(track_info)
        print()
    return render_template('index.html')
