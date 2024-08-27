from flask import Flask, request, jsonify
from flask import render_template
from .spo2yt import Spo2yt
from datetime import datetime as time
from dotenv import load_dotenv
from google.oauth2 import id_token
# from celery import Celery
# from make_celery import make_celery

app = Flask(__name__)
app.secret_key = 'q3239fbasnqlpdpwep'  # change to point to env

# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379/0',
#     CELERY_RESULT_BACKEND='redis://localhost:6379/0'
# )
# celery = make_celery(app)

load_dotenv()

my_app = Spo2yt()

@app.route("/")
def index():
    """ Index page
        Returns all your current saved playlists
    """
    playlists = my_app.get_spotify_playlists()
    return render_template('index.html', playlists=playlists)

    
@app.route('/preview/<string:playlist_id>/', strict_slashes=False, methods=['GET'])
def preview_playlist_conversion(playlist_id):
    name, tracks, image = my_app.get_spotify_playlist_tracks(playlist_id)
    return render_template('playlist.html', name=name, tracks=tracks, image=image, p_id=playlist_id)


@app.route('/convert/<string:playlist_id>', strict_slashes=False, methods=['GET', 'POST'])
def convert_playlist(playlist_id):
    name, tracks, _ = my_app.get_spotify_playlist_tracks(playlist_id)
    try:
        p_id = my_app.create_youtube_music_playlist(name, tracks)
    except Exception as e:
        print(f'An exception occured: {e}')
        try:
             # incase of interruption (Quotas or other errors)
            link = my_app.get_yt_playlist_music_videos(p_id)[0]
        except Exception:
            link = None
        # app.logger.info(f"[{time.now()}]: {e}")
        # flash('An error occurred while converting, try again later')
    else:
        video_1 = my_app.get_yt_playlist_music_videos(p_id)[0]
        link = f"https://music.youtube.com/watch?v={video_1}&list={p_id}&autoplay=1"
    
    print(f"Link to youtube music playlist: {link}")
    return jsonify({'link': link})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
