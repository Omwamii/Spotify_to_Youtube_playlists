""" Module with Base class """
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Read spotify client id
"""
f_cl_id = open("sp_client_id", "r")
cl_id = f_cl_id.read()
f_cl_id.close()

# Read spotify client secret
f_cl_secret = open("sp_client_secret", "r")
cl_secret = f_cl_secret.read()
f_cl_secret.close()

os.environ['SPOTIPY_CLIENT_ID'] = cl_id
os.environ['SPOTIPY_CLIENT_SECRET'] = cl_secret
os.environ['SPOTIPY_REDIRECT_URI'] = "http://127.0.0.1:5000"
"""

os.environ['SPOTIPY_CLIENT_ID'] = "395b4027785749e8be658134aa307d07"
os.environ['SPOTIPY_CLIENT_SECRET'] = "b11e8fc5ea1146098df771eef2613c96"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://127.0.0.1:5000"

class Base():
    """ Base class with youtube's google auth & spotify auth"""
    creds, flow, data = (None, None, None)

    # scopes for youtube & spotify
    __yt_scope = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.upload"
            ]
    __sp_scope = """
                user-library-read
                playlist-read-private
                playlist-read-collaborative
                """

    def __init__(self):
        """ Initialize authentication """
        if os.path.exists("token.json"):
            # The file token.json stores the user's access and refresh tokens
            # and is created automatically when the auth flow completes
            # for the first time
            self.creds = Credentials.from_authorized_user_file('token.json',
                                                               self.__yt_scope)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # credentials file downloaded to root from google cloud console
                self.flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", self.__yt_scope)
                self.creds = self.flow.run_local_server(
                        port=8080, access_type='offline', prompt='consent')
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        try:
            # setup google classroom api
            self.youtube = build("youtube", "v3", credentials=self.creds)
        except HttpError as error:
            # Error with classroom API
            print(f"Youtube Data API error: {error}")
        try:
            self.spotify = spotipy.Spotify(
                auth_manager=SpotifyOAuth(scope=self.__sp_scope))
        except spotipy.oauth2.SpotifyOauthError as e:
            print("Authentication failed :(")
            print(e)


if __name__ == "__main__":
    app = Base()  # cl tests
