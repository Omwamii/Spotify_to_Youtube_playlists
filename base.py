""" Module with Base class """
import os
import time
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import logger
from dotenv import load_dotenv
from .tokens import yt_token_files

load_dotenv()

class Base():
    """ Base class with youtube's google auth & spotify auth"""
    creds, flow, data = (None, None, None)
    __current_toke_file = 0
    _youtube_api_token_files = yt_token_files

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
        # TODO after app passed testing stage, change to automatic refresh token

        if os.path.exists("token.json"):
            self.authenticate_from_existing_token_file()

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    # failed to refresh, delete token & start again
                    app.logger.info(f"[{time.now()}]: {e}")
                    os.remove('token.json')
                    self.create_token_from_credentials_file()
            else:
                self.create_token_from_credentials_file()
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            # setup Youtube data api
            self.youtube = build("youtube", "v3", credentials=self.creds)
        except HttpError as error:
            # Error with classroom API
            # app.logger.info(f"[{time.now()}]: {error}")
            pass

        try:
            self.spotify = spotipy.Spotify(
                auth_manager=SpotifyOAuth(scope=self.__sp_scope))
        except spotipy.oauth2.SpotifyOauthError as e:
            # app.logger.info(f"[{time.now()}]: {e}")
            pass

    def authenticate_from_existing_token_file(self):
        """ Authenticate from existing token file"""
            
        # The file token.json stores the user's access and refresh tokens
        # and is created automatically when the auth flow completes
        # for the first time
        self.creds = Credentials.from_authorized_user_file('token.json',
                                                               self.__yt_scope)
        
    def create_token_from_credentials_file(self):
        """ Create authentication token from credentials """
        # credentials file downloaded to root from google cloud console
        self.flow = InstalledAppFlow.from_client_secrets_file(
                            "credentials3.json", self.__yt_scope)
        self.creds = self.flow.run_local_server(
            port=8080, access_type='offline', prompt='consent')


if __name__ == "__main__":
    app = Base()  # cl tests