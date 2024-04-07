""" Class with youtube + spotify api resources """
from base import Base


class Spo2yt(Base):
    """ Complete class with spotify & youtube music resources """
    def get_spotify_playlists(self):
        playlists = self.spotify.current_user_playlists().get('items')
        p_info = list()
        for playlist in playlists:
            image_url = playlist.get('images')[0].get('url') if playlist.get('images') else None
            data = {'id': playlist.get('id'), 'name': playlist.get('name'),
                    'cover': image_url, 'tracks': playlist.get('tracks').get('total')}
            p_info.append(data)
        return p_info

    def get_spotify_playlist_tracks(self, playlist_id: str):
        if not playlist_id:
            return []
        playlist = self.spotify.playlist(playlist_id)
        tracks = list()
        for item in playlist['tracks'].get('items'):
            # tracks.append(item)
            if item.get('track'):
                # for some reason, there exists some empty song items
                data = {'id': item['track']['id'], 'name': item['track']['name']}
                tracks.append(data)
        return tracks
