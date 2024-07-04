from flask import Flask, request, jsonify
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
    # p_id = my_app.create_youtube_music_playlist(name, tracks)
    # video_1 = my_app.get_yt_playlist_music_videos(p_id)[0]
    return render_template('playlist.html', name=name, tracks=tracks)

@app.route('/create-playlist/', methods=['POST'])
def create_youtube_music_playlist():
    songs_to_add = request.get_json()
    # p_id = my_app.create_youtube_music_p
    return "Redirecting to youtube playlists"
    
@app.route('/preview/<string:playlist_id>/', strict_slashes=False, methods=['GET'])
def preview_playlist_conversion(playlist_id):
    name, tracks, image = my_app.get_spotify_playlist_tracks(playlist_id)
    return render_template('playlist.html', name=name, tracks=tracks, image=image)

@app.route('/api/convert', methods=['POST'])
def convert_playlist():
    data = request.json
    try:
        p_id = my_app.create_youtube_music_playlist(data['name'], data['tracks'])
    except Exception as e:
        print(f'an exception occured: {e}')
        status = 'error'
        link = None
    else:
        status = 'OK'
        video_1 = my_app.get_yt_playlist_music_videos(p_id)[0]
        link = f"https://music.youtube.com/watch?v={video_1}&list={p_id}&autoplay=1"
    response = {
        'status': status,
        'link': link
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
