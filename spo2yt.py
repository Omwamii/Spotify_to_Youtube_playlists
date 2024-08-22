import time
from base import Base
from typing import Any, List, Dict

class RateLimiter:
    """ Simple rate limiter to control the flow of API requests (make use of per minute quota)"""
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        
    def wait(self):
        print('<<< waiting >>>')
        now = time.time()
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.pop(0)
        
        if len(self.calls) >= self.max_calls:
            time.sleep(self.period - (now - self.calls[0]))
            self.calls.pop(0)
        
        self.calls.append(time.time())

class Spo2yt(Base):
    """ Complete class with Spotify & YouTube Music resources """
    def __init__(self):
        super().__init__()
        self.rate_limiter = RateLimiter(max_calls=1800, period=60)  # e.g., 1800 calls per minute

    def get_spotify_playlists(self) -> List[Dict[str, Any]]:
        """ Get all your current saved Spotify playlists """
        self.rate_limiter.wait()
        print()
        print('Getttig spotify playlists')
        playlists = self.spotify.current_user_playlists().get('items')
        p_info = list()
        for playlist in playlists:
            image_url = playlist.get('images')[0].get('url') if playlist.get('images') else None
            data = {'id': playlist.get('id'), 'name': playlist.get('name'),
                    'cover': image_url, 'tracks': playlist.get('tracks').get('total')}
            p_info.append(data)
        return p_info

    def get_spotify_playlist_tracks(self, playlist_id: str) -> Any:
        """ Get song tracks for a Spotify playlist """
        print()
        print('getting spotify tracks')
        if not playlist_id:
            return []
        self.rate_limiter.wait()
        playlist = self.spotify.playlist(playlist_id)
        p_name = playlist['name']
        tracks = list()
        for item in playlist['tracks'].get('items'):
            if item.get('track'):
                artists = ""
                artist_names = item['track']['artists']
                for artist in artist_names:
                    artists += f" {artist['name']}"
                data = {'id': item['track']['id'], 'name': item['track']['name'],
                        'artists': artists}
                tracks.append(data)
        image = playlist.get('images')[0].get('url') if playlist.get('images') else None
        return (p_name, tracks, image)

    def search_song_youtube(self, song_name: str, song_artists: str) -> Any:
        """ Search for a song and return info else return None """
        print()
        print('searching song on youtube')
        if not song_name:
            return None
        search_string = song_name + song_artists
        kwargs = {'q': search_string, 'maxResults': 10}
        self.rate_limiter.wait()
        return self.youtube.search().list(part='id,snippet', **kwargs).execute().get('items')[0]

    def create_youtube_music_playlist(self, p_name: str, songs: List[Dict[str, Any]]) -> Any:
        """ Create youtube music playlist
            INSERT QUOTA COST: 50 units
            LIST QUOTA COST: 1 unit
        """
        print()
        print('creating youtube playlist')
        """ Creates a YouTube playlist from a list of songs """
        part = 'id,snippet,status,contentDetails'
        resource = {'kind': "youtube#playlist", "snippet": {'title': p_name, 'defaultLanguage': 'en'}}
        playlist_exists = False
        yt_playlist = None

        self.rate_limiter.wait()
        print('about to list')
        my_yt_playlists = self.youtube.playlists().list(part=part, mine=True).execute().get('items')
        print('have listed')

        for playlist in my_yt_playlists:
            if playlist['snippet']['title'] == p_name:
                playlist_exists = True
                yt_playlist = {'id': playlist['id']}
                break

        if not playlist_exists:
            print('about to instert')
            self.rate_limiter.wait()
            try:
                yt_playlist = self.youtube.playlists().insert(part=part, body=resource).execute()
            except Exception:
                time.sleep(60)
                try:
                    yt_playlist = self.youtube.playlists().insert(part=part, body=resource).execute()
                except Exception as e:
                    print()
                    print(f'Error occured again : {e}')
                    print()
            print('have inserted')
        
        if yt_playlist:
            for song in songs:
                self.add_song_to_yt_playlist(song['name'], song['artists'], yt_playlist['id'])
            print('done converting playlist >>>')
        return yt_playlist['id']

    def get_yt_playlist_music_videos(self, playlist_id: str) -> Any:
        """" Get videos info in a youtube playlist"""
        print()
        print('getting youtube music videos')
        part = 'id,snippet,status,contentDetails'
        video_ids = list()
        self.rate_limiter.wait()
        playlist_videos = self.youtube.playlistItems().list(part=part, playlistId=playlist_id).execute().get('items')
        
        for video in playlist_videos:
            video_ids.append(video['contentDetails']['videoId'])
        return video_ids
    
    def add_song_to_yt_playlist(self, song: str, song_artists: str, playlist_id: str) -> Any:
        """ Adds a song to a playlist, checking whether the song already exists in playlist.
            If song already exists, returns None.
            QUOTA COST: 50 units
        """
        print()
        print('adding song to youtube playlist')
        yt_song = self.search_song_youtube(song, song_artists)
        part = 'id,snippet,status,contentDetails'
        if yt_song['id']['videoId'] in self.get_yt_playlist_music_videos(playlist_id):
            # Song is already in playlist
            return
        insert_data = {'kind': "youtube#playlistItem", 'snippet': {'playlistId': playlist_id, 'resourceId': yt_song.get('id')}}
        self.rate_limiter.wait()
        self.youtube.playlistItems().insert(part=part, body=insert_data).execute()


