from rest_framework import serializers
from .models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Check that an artist with the same name doesn't already exist.
        """
        if self.instance is None:
            if Artist.objects.filter(name=data["name"]).exists():
                raise serializers.ValidationError("An artist with the same name already exists.")
        return data

class AlbumSerializer(serializers.ModelSerializer):
    # artist = ArtistSerializer()
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())

    class Meta:
        model = Album
        fields = ['id', 'name', 'artist', 'release_date', 'genre_name', 'collection_price', 'currency', 'artwork_url', 'collection_view_url', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Check that a song with the same name, artist and album doesn't already exist.
        """
        if self.instance is None:
            # Creating a new instance
            if Album.objects.filter(name=data['name'], artist=data['artist']).exists():
                raise serializers.ValidationError("An album with the same name and artist already exists.")

        return data
    
    def create(self, validated_data):
        artist = validated_data.pop('artist')
        album = Album.objects.create(**validated_data, artist=artist)
        return album

class SongSerializer(serializers.ModelSerializer):
    # artist = ArtistSerializer()
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    # album = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())

    class Meta:
        model = Song
        fields = ['id', 'name', 'artist', 'album', 'release_date', 'genre_name', 'track_price', 'currency', 'track_view_url', 'preview_url', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Check that a song with the same name, artist and album doesn't already exist.
        """
        if self.instance is None:
            # Creating a new instance
            if Song.objects.filter(name=data['name'], artist=data['artist'], album=data['album']).exists():
                raise serializers.ValidationError("A song with the same name, artist and album already exists.")

        return data
    
    def create(self, validated_data):
        artist = validated_data.pop('artist')
        album = Song.objects.create(**validated_data, artist=artist)
        return album
