import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials

try:
    SPOTIFY_CLIENT = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        )
    )
except:
    print("Error Please assign SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.")
    exit(1)
