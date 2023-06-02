import random
from django.conf import settings
from core.api.serializers import TrackResponseSerializer, TrackSerializer
from core.constants import GENRES
from core.spotify_handler import SPOTIFY_CLIENT
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class TrackAPI(APIView):
    """
    Tracks API list random popular songs
    """

    def post(self, request, genre, format=None):
        genre_artist = GENRES.get(genre)
        if not genre_artist:
            serializers.ValidationError("Genre not found.")
        artist = random.choice(genre_artist)
        results = SPOTIFY_CLIENT.search(
            q="artist:" + artist, type="track", limit=settings.SPOTIFY_TRACK_LIMIT
        )
        items = results["tracks"]["items"]

        random_tracks = random.choices(items, k=10)
        sorted(random_tracks, key=lambda d: d["popularity"], reverse=True)
        serializer = TrackResponseSerializer(random_tracks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
