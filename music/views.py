from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
import requests
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from music.models import Artist, Album, Song
from music.serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from music.filters import ArtistFilter, AlbumFilter, SongFilter
from music.tasks import seed_music_data_task

class ArtistFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

class ArtistList(APIView):
    """
    List all artists, or create a new artists.
    """
    def get(self, request, format=None):
        artists = Artist.objects.all()
        artist_filter = ArtistFilter(request.GET, queryset=artists)
        serializer = ArtistSerializer(artist_filter.qs, many=True)
        return Response(serializer.data)

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ArtistFilter
    ordering_fields = ['name']

    def post(self, request, format=None):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistDetail(APIView):
    """
    Retrieve, update or delete an artist instance.
    """
    def get_object(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        artist = self.get_object(pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        artist = self.get_object(pk)
        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        artist = self.get_object(pk)
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AlbumList(APIView):
    """
    List all albums, or create a new albums.
    """
    def get(self, request, format=None):
        albums = Album.objects.all()
        album_filter = AlbumFilter(request.GET, queryset=albums)
        serializer = AlbumSerializer(album_filter.qs, many=True)
        return Response(serializer.data)
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AlbumFilter
    ordering_fields = ['name', 'artist_name', 'genre_name']


    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetail(APIView):
    """
    Retrieve, update or delete an album instance.
    """
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SongList(APIView):
    """
    List all songs, or create a new song.
    """
    def get(self, request, format=None):
        songs = Song.objects.all()
        song_filter = SongFilter(request.GET, queryset=songs)
        serializer = SongSerializer(song_filter.qs, many=True)
        return Response(serializer.data)
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AlbumFilter
    ordering_fields = ['album', 'artist', 'artist_name', 'genre_name']

    def post(self, request, format=None):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SongDetail(APIView):
    """
    Retrieve, update or delete a song instance.
    """
    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        song = self.get_object(pk)
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class SeedDataView(APIView):
#     def maybe_create_artist(self, name):
#         artist =  Artist.objects.filter(name=name).first()
#         if artist is None:
#             artist_serializer = ArtistSerializer(data={
#                 'name': name
#             })
#             if artist_serializer.is_valid():
#                 artist = artist_serializer.save()
#                 artist_serializer = ArtistSerializer(artist)
#             return artist_serializer.data
#         else:
#             artist_serializer = ArtistSerializer(artist)
#             return artist_serializer.data
        
#     def maybe_create_album(self, album_data, artist):
#         album =  Album.objects.filter(name=album_data['collectionName'], artist=artist['id']).first()
       
#         if album is None:
#             try:
#                 album_serializer = AlbumSerializer(data={
#                                         'name': album_data['collectionName'],
#                                         'artist': artist['id'],
#                                         'release_date': album_data['releaseDate'],
#                                         'genre_name': album_data['primaryGenreName'],
#                                         'collection_price': album_data['collectionPrice'],
#                                         'currency': album_data['currency'],
#                                         'artwork_url': album_data['artworkUrl100'],
#                                         'collection_view_url': album_data['collectionViewUrl']
#                                     })
#                 if album_serializer.is_valid():
#                     album = album_serializer.save()
#                     album_serializer = AlbumSerializer(album)
#                 return album_serializer.data
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 print(album_data)
#                 return None
            
            
#         else:
#             album_serializer = AlbumSerializer(album)
#             return album_serializer.data
    
#     def maybe_create_song(self, song_data, artist, album):
#         song = None
#         try:
#             song =  Song.objects.filter(name=song_data['trackName'], artist=artist['id'], album=album['id']).first()
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             print(song_data)
#             print(artist)
#             print(album)
#             return None
       
#         if song is None:
#             try:
#                 song_serializer = SongSerializer(data={
#                                                     'name': song_data['trackName'],
#                                                     'artist': artist['id'],
#                                                     'album': album['id'],
#                                                     'release_date': song_data['releaseDate'],
#                                                     'genre_name': song_data['primaryGenreName'],
#                                                     'track_price': song_data['trackPrice'],
#                                                     'currency': song_data['currency'],
#                                                     'track_view_url': song_data['trackViewUrl'],
#                                                     'preview_url': song_data['previewUrl']
#                                                 })
                                                
#                 if song_serializer.is_valid():
#                     song_serializer.save()
#                     song_serializer = SongSerializer(song)
#                 return song_serializer.data
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 print(song_data)
#                 print(artist)
#                 print(album)
#                 return None
#         else:
#             song_serializer = SongSerializer(song)
#             return song_serializer.data
       
    
#     def post(self, request):
        artists = request.data.get('artists', [])
        if not artists:
            return Response({'error': 'No artist provided'}, status=status.HTTP_400_BAD_REQUEST)
        for artist_name in artists:
            # Search for artist in itunes api
            url = 'https://itunes.apple.com/search'
            params = {'term': artist_name, 'entity': 'musicArtist'}
            response = requests.get(url, params=params)

            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                results = data.get('results', [])

                if results:
                    # create artists object
                    artist_data = results[0]
                    artist = self.maybe_create_artist(artist_data['artistName'])
                    
                    if artist:
                        # Fetch the albums for the artist
                        url = 'https://itunes.apple.com/lookup'
                        params = {'id': artist_data['artistId'], 'entity': 'album'}
                        response = requests.get(url, params=params)

                        if response.status_code == status.HTTP_200_OK:
                            data = response.json()
                            results = data.get('results', [])

                            albums_data = [item for item in results if item.get("wrapperType") == "collection"]

                            for album_data in albums_data:
                                album = self.maybe_create_album(album_data, artist)
                                
                                if album and album is not None:
                                    # Fetch the songs for the album
                                    url = 'https://itunes.apple.com/lookup'
                                    params = {'id': album_data['collectionId'], 'entity': 'song'}
                                    response = requests.get(url, params=params)
                                    if response.status_code == status.HTTP_200_OK:
                                        data = response.json()
                                        results = data.get('results', [])
                                        songs_data = [item for item in results if item.get("wrapperType") == "track"]
                                        
                                        for song_data in songs_data:
                                            self.maybe_create_song(song_data, artist, album)
                                           
                                

        return Response({'message': 'Data seeding completed'}, status=status.HTTP_200_OK)
    
class SeedDataView(APIView):
    def post(self, request):
        artists = request.data.get('artists')
        for artist in artists:
            # Spawn a new Celery task for each artist
            seed_music_data_task.apply_async(args=[artist])
        return Response({'message': 'Data processing and seeding ongoing'})