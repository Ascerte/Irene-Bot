import praw
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

reddit_api = praw.Reddit(client_id =,
                      client_secret =,
                      username =,
                      password =,
                      user_agent ='Irene Bot')


client_credentials_manager = SpotifyClientCredentials(client_id=,
                                                      client_secret=)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)