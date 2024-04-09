from flask import Flask
from flask import render_template
from spo2yt import Spo2yt

app = Flask(__name__)

my_app = Spo2yt()

@app.route("/")
def index():
    """ Index page
        Returns all your current saved playlists
    """
    playlists = my_app.get_spotify_playlists()
    return render_template('index.html', playlists=playlists)

@app.route('/playlist/<string:play_id>')
def goto_spotify_playlist(play_id:str):
    """ Goes to page for specific playlist """
    name, tracks = my_app.get_spotify_playlist_tracks(play_id)
    res = my_app.create_youtube_music_playlist(name, tracks)
    # print(my_app.search_song_youtube('fever'))
    # name, tracks = [], []
    return render_template('playlist.html', name=name, tracks=tracks)

@app.route('/create-playlist/')
def create_youtube_music_playlist(songs):
    return "Redirecting to youtube playlists"
    

if __name__ == "__main__":
    app.run(debug=True, port=8080)
