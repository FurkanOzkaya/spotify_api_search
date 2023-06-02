from rest_framework import serializers


class TrackSerializer(serializers.Serializer):
    genre = serializers.CharField()


class TrackResponseSerializer(serializers.Serializer):
    artist = serializers.SerializerMethodField()
    track = serializers.CharField(source="name")
    album_image_url = serializers.SerializerMethodField()
    preview_url = serializers.CharField()

    def get_artist(self, obj):
        return obj["artists"][0]["name"]

    def get_album_image_url(self, obj):
        return obj["album"]["images"][0]["url"]

    def validate(self, attrs):
        return super().validate(attrs)
