from django_filters import rest_framework as filters
from .models import Song, Artist, Album


class ArtistFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Song
        fields = ['name']

class AlbumFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    genre_name = filters.CharFilter(field_name='genre_name', lookup_expr='icontains')
    artist_name = filters.CharFilter(field_name='artist__name', lookup_expr='icontains')

    class Meta:
        model = Song
        fields = ['artist', 'artist_name', 'genre_name']

class SongFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    genre_name = filters.CharFilter(field_name='genre_name', lookup_expr='icontains')
    artist_name = filters.CharFilter(field_name='album__artist__name', lookup_expr='icontains')

    class Meta:
        model = Song
        fields = ['album', 'artist', 'artist_name', 'genre_name']