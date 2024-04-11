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
        """ Get song tracks for a spotify playlist """
        if not playlist_id:
            return []
        playlist = self.spotify.playlist(playlist_id)
        p_name = playlist['name']
        tracks = list()
        for item in playlist['tracks'].get('items'):
            if item.get('track'):
                # for some reason, there exists some empty song items
                artists = ""
                artist_names = item['track']['artists']
                for artist in artist_names:
                    artists += f" {artist['name']}"
                data = {'id': item['track']['id'], 'name': item['track']['name'],
                        'artists': artists}
                tracks.append(data)
        return (p_name, tracks)

    def search_song_youtube(self, song_name: str, song_artists: str) -> Any:
        """ Search for song and return info else return None """
        if not song_name:
            return None
        search_string = song_name + song_artists
        kwargs = {'q': search_string, 'maxResults': 10}
        return self.youtube.search().list(part='id,snippet', **kwargs).execute().get('items')[0]

    def create_youtube_music_playlist(self, p_name: str, songs: list) -> Any:
        """ Creates a youtube playlist from a list of songs """
        part = 'id,snippet,status,contentDetails'
        resource = {'kind': "youtube#playlist", "snippet": {'title': p_name, 'defaultLanguage': 'en'}}
        new_play = False
        my_yt_playlists = self.youtube.playlists().list(part=part, mine=True).execute().get('items')

        for playlist in my_yt_playlists:
            if playlist['snippet']['title'] == p_name:
                # playlist had already been created
                new_play = True
                yt_playlist = {'id': playlist['id']}
                break

        if not new_play:
            # create a new playlist if no playlist by the title exists
            yt_playlist = self.youtube.playlists().insert(part=part, body=resource).execute()
        
        if yt_playlist:
            for song in songs:
                    res = self.add_song_to_yt_playlist(song['name'], song['artists'], yt_playlist['id'])
                    if not res:
                        # song video already exists in playlist
                        print(f"{song['name']} already exists in playlist")
                    else:
                        # print(f"Response after inserting {song['name']}: {res}")
                        pass

        return yt_playlist['id']
    
    def get_yt_playlist_music_videos(self, playlist_id: str) -> Any:
        part = 'id,snippet,status,contentDetails'
        video_ids = list()
        playlist_videos = self.youtube.playlistItems().list(part=part, playlistId=playlist_id).execute().get('items')
        
        for video in playlist_videos:
            video_ids.append(video['contentDetails']['videoId'])
        return video_ids
    
    def add_song_to_yt_playlist(self, song: str, song_artists: str, playlist_id: str) -> Any:
        """ Adds a song to a playlist, checking whether the song already exists in playlist
            If song already exists, returns None
        """
        yt_song = self.search_song_youtube(song, song_artists)
        part = 'id,snippet,status,contentDetails'
        if yt_song['id']['videoId'] in self.get_yt_playlist_music_videos(playlist_id):
            # song is already in playlist
            return None
        insert_data = {'kind': "youtube#playlistItem", 'snippet': {'playlistId': playlist_id, 'resourceId': yt_song.get('id')}}
        res = self.youtube.playlistItems().insert(part=part, body=insert_data).execute()
        return res
