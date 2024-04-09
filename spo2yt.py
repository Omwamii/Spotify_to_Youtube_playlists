""" Class with youtube + spotify api resources """
from base import Base
from typing import Any

class Spo2yt(Base):
    """ Complete class with spotify & youtube music resources """
    def get_spotify_playlists(self):
        """ Get all your current saved spotify playlists """
        playlists = self.spotify.current_user_playlists().get('items')
        p_info = list()
        for playlist in playlists:
            image_url = playlist.get('images')[0].get('url') if playlist.get('images') else None
            data = {'id': playlist.get('id'), 'name': playlist.get('name'),
                    'cover': image_url, 'tracks': playlist.get('tracks').get('total')}
            p_info.append(data)
        return p_info

    def get_spotify_playlist_tracks(self, playlist_id: str) -> Any:
        """ Get tracks for a spotify playlist """
        if not playlist_id:
            return []
        playlist = self.spotify.playlist(playlist_id)
        p_name = playlist['name']
        tracks = list()
        for item in playlist['tracks'].get('items'):
            # tracks.append(item)
            if item.get('track'):
                # for some reason, there exists some empty song items
                data = {'id': item['track']['id'], 'name': item['track']['name']}
                tracks.append(data)
        return (p_name, tracks)

    def search_song_youtube(self, song_name: str) -> Any:
        """ Search for song and return info else return None """
        if not song_name:
            return None
        kwargs = {'q': song_name, 'maxResults': 10}
        return self.youtube.search().list(part='id,snippet', **kwargs).execute().get('items')[0]

    def create_youtube_music_playlist(self, p_name: str, songs: list) -> Any:
        """ Creates a youtube playlist from a list of songs """
        # part = 'id,snippet,status,localizations,contentDetails'
        part = 'id,snippet,status,contentDetails'
        resource = {'kind': "youtube#playlist", "snippet": {'title': p_name, 'defaultLanguage': 'en'}}
        new_play = False
        my_yt_playlists = self.youtube.playlists().list(part=part, mine=True).get('items')

        for playlist in my_yt_playlists:
            if playlist['snippet']['title'] == p_name:
                # playlist had already been created
                new_play = True
                print('playlist had already been created')
                yt_playlist = {'id': playlist['id']}
                break

        if not new_play:
            print("Creating a new playlist....")
            yt_playlist = self.youtube.playlists().insert(part=part, body=resource).execute()

        if yt_playlist:
            for song in songs:
                yt_song = self.search_song_youtube(song.get('name'))
                insert_data = {'kind': "youtube#playlistItem", 'snippet': {'playlistId': yt_playlist.get('id'), 'resourceId': yt_song.get('id')}}
                res = self.youtube.playlistItems().insert(part=part, body=insert_data).execute()
                print(f"Response after inserting playlist item: {res}")

        return yt_playlist
    
    def add_song_to_existing_yt_playlist(self, song: str, playlist_id: str) -> Any:
        """ Adds a song to an existing playlist
        """
        yt_song = self.search_song_youtube(song)
        part = 'id,snippet,status,contentDetails'
        try:
             insert_data = {'kind': "youtube#playlistItem", 'snippet': {'playlistId': playlist_id, 'resourceId': yt_song.get('id')}}
             self.youtube.playlistItems().insert(part=part, body=insert_data).execute()
        except Exception as e:
            # probably sth like item already exists
            print(f'Error when adding song:  {e}')