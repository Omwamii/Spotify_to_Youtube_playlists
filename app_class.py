""" Module with App class """
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class App():
    """ App class with functionalities """
    creds, flow, data = (None, None, None)
    _SCOPES = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.upload"
            ]

    def __init__(self):
        """ Initialize authentication """
        if os.path.exists("token.json"):
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            self.creds = Credentials.from_authorized_user_file('token.json', self._SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
            else:
                # credentials file was downloaded to root from google cloud console credential
                self.flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self._SCOPES)
                self.creds = self.flow.run_local_server(port=8080, access_type='offline', prompt='consent')
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        try:
            # setup google classroom api
            self.youtube = build("youtube", "v3", credentials=self.creds)
        except HttpError as error:
            # Error with classroom API
            print(f"Youtube Data API error: {error}")
        else:
            # calling classroom API to fetch course data
            self.data = self.youtube.search().list(
                    part='id,snippet'
                    ).execute()
            print(self.data)

if __name__ == "__main__":
    app = App()
    print(app.data)
