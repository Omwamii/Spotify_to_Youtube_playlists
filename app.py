from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
from spo2yt import Spo2yt
from celery import Celery
from make_celery import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
celery = make_celery(app)

my_app = Spo2yt()

@app.route("/")
def index():
    """ Index page
        Returns all your current saved playlists
    """
    playlists = my_app.get_spotify_playlists()
    return render_template('index.html', playlists=playlists)

# @app.route('/playlist/<string:play_id>')
# def goto_spotify_playlist(play_id:str):
#     """ Goes to page for specific playlist """
#     name, tracks = my_app.get_spotify_playlist_tracks(play_id)
#     # p_id = my_app.create_youtube_music_playlist(name, tracks)
#     # video_1 = my_app.get_yt_playlist_music_videos(p_id)[0]
#     print(play_id)
#     return render_template('playlist.html', name=name, tracks=tracks, p_id=play_id)
    
@app.route('/preview/<string:playlist_id>/', strict_slashes=False, methods=['GET'])
def preview_playlist_conversion(playlist_id):
    name, tracks, image = my_app.get_spotify_playlist_tracks(playlist_id)
    return render_template('playlist.html', name=name, tracks=tracks, image=image, p_id=playlist_id)

@app.route('/progress/<task_id>')
def show_progress(task_id):
    return render_template('progress.html', task_id=task_id)

@celery.task(bind=True)
def convert_playlist_task(self, name, tracks):
    total = len(tracks)
    for i, track in enumerate(tracks):
        # Simulate conversion process
        # my_app.convert_track_to_youtube(track)
        self.update_state(state='PROGRESS',
                          meta={'current': i + 1, 'total': total})
    p_id = my_app.create_youtube_music_playlist(name, tracks)
    return {'current': total, 'total': total, 'status': 'Task completed!', 'p_id': p_id}

# @app.route('/convert/<string:playlist_id>', methods=['POST'])
# def convert_playlist(playlist_id):
#     name, tracks, _ = my_app.get_spotify_playlist_tracks(playlist_id)
#     task = convert_playlist_task.apply_async(args=[name, tracks])
#     return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/convert/<string:playlist_id>', methods=['POST'])
def convert_playlist(playlist_id):
    name, tracks, _ = my_app.get_spotify_playlist_tracks(playlist_id)
    task = convert_playlist_task.apply_async(args=[name, tracks])
    # Redirect to the progress page
    return redirect(url_for('show_progress', task_id=task.id))


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = convert_playlist_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info)
        }
    return jsonify(response)


# @app.route('/convert/<string:playlist_id>', strict_slashes=False)
# def convert_playlist(playlist_id):
#     name, tracks, _ = my_app.get_spotify_playlist_tracks(playlist_id)
#     try:
#         p_id = my_app.create_youtube_music_playlist(name, tracks)
#     except Exception as e:
#         print(f'An exception occured: {e}')
#         link = None
#     else:
#         video_1 = my_app.get_yt_playlist_music_videos(p_id)[0]
#         link = f"https://music.youtube.com/watch?v={video_1}&list={p_id}&autoplay=1"
#     if link:
#         return redirect(link)
#     else:
#         # HERE I WANT IT TO DIRECT TO A PAGE, SHOWING A PROGRESS BAR AS IT CONVERRS THE PLAYLIST IN THE BACKGROUND
#         return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)
