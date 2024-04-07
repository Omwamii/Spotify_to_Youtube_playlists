""" Class with youtube + spotify api resources """
from base import Base


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

    def get_spotify_playlist_tracks(self, playlist_id: str):
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

    def search_song_youtube(self, song_name: str):
        """ Search for song and return info else return None """
        if not song_name:
            return None
        kwargs = {'q': song_name, 'maxResults': 10}
        return self.youtube.search().list(part='id,snippet', **kwargs).execute().get('items')[0]

    def create_youtube_music_playlist(self, p_name: str, songs: list):
        """ Creates a youtube playlist from a list of songs """
        # part = 'id,snippet,status,localizations,contentDetails'
        part = 'id,snippet,status,contentDetails'
        resource = {'kind': "youtube#playlist", "snippet": {'title': p_name, 'defaultLanguage': 'en'}}
        yt_playlist = self.youtube.playlists().insert(part=part, body=resource).execute()
        if yt_playlist:
            for song in songs:
                insert_data = {'kind': "youtube#playlistItem", 'snippet': {'playlistId': yt_playlist.get('id'), 'resourceId': {'kind': "youtube#video", 'videoId': song.get('id')}}}
                res = self.youtube.playlistItems().insert(part=part, body=insert_data).execute()
                print(f"Response after inserting playlist item: {res}")
        return yt_playlist
