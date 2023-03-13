# from rest_framework import status
# import requests
# import django
# django.setup()


# from music.models import Artist, Album, Song
# from music.serializers import ArtistSerializer, AlbumSerializer, SongSerializer

    
# def seed_data(artist_name):
#     url = 'https://itunes.apple.com/search'
#     params = {'term': artist_name, 'entity': 'musicArtist'}
#     response = requests.get(url, params=params)

#     if response.status_code == status.HTTP_200_OK:
#         data = response.json()
#         results = data.get('results', [])

#         if results:
#             # create artists object
#             artist_data = results[0]
#             artist = maybe_create_artist(artist_data['artistName'])
            
#             if artist:
#                 # Fetch the albums for the artist
#                 url = 'https://itunes.apple.com/lookup'
#                 params = {'id': artist_data['artistId'], 'entity': 'album'}
#                 response = requests.get(url, params=params)

#                 if response.status_code == status.HTTP_200_OK:
#                     data = response.json()
#                     results = data.get('results', [])

#                     albums_data = [item for item in results if item.get("wrapperType") == "collection"]

#                     for album_data in albums_data:
#                         album = maybe_create_album(album_data, artist)
                        
#                         if album and album is not None:
#                             # Fetch the songs for the album
#                             url = 'https://itunes.apple.com/lookup'
#                             params = {'id': album_data['collectionId'], 'entity': 'song'}
#                             response = requests.get(url, params=params)
#                             if response.status_code == status.HTTP_200_OK:
#                                 data = response.json()
#                                 results = data.get('results', [])
#                                 songs_data = [item for item in results if item.get("wrapperType") == "track"]
                                
#                                 for song_data in songs_data:
#                                     maybe_create_song(song_data, artist, album)
                                    
                        

#     return 


# def maybe_create_artist(name):
#     artist =  Artist.objects.filter(name=name).first()
#     if artist is None:
#         artist_serializer = ArtistSerializer(data={
#             'name': name
#         })
#         if artist_serializer.is_valid():
#             artist = artist_serializer.save()
#             artist_serializer = ArtistSerializer(artist)
#         return artist_serializer.data
#     else:
#         artist_serializer = ArtistSerializer(artist)
#         return artist_serializer.data
    
# def maybe_create_album(album_data, artist):
#     album =  Album.objects.filter(name=album_data['collectionName'], artist=artist['id']).first()
    
#     if album is None:
#         try:
#             album_serializer = AlbumSerializer(data={
#                                     'name': album_data['collectionName'],
#                                     'artist': artist['id'],
#                                     'release_date': album_data['releaseDate'],
#                                     'genre_name': album_data['primaryGenreName'],
#                                     'collection_price': album_data['collectionPrice'],
#                                     'currency': album_data['currency'],
#                                     'artwork_url': album_data['artworkUrl100'],
#                                     'collection_view_url': album_data['collectionViewUrl']
#                                 })
#             if album_serializer.is_valid():
#                 album = album_serializer.save()
#                 album_serializer = AlbumSerializer(album)
#             return album_serializer.data
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             print(album_data)
#             return None
        
        
#     else:
#         album_serializer = AlbumSerializer(album)
#         return album_serializer.data

# def maybe_create_song(song_data, artist, album):
#     song = None
#     try:
#         song =  Song.objects.filter(name=song_data['trackName'], artist=artist['id'], album=album['id']).first()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         print(song_data)
#         print(artist)
#         print(album)
#         return None
    
#     if song is None:
#         try:
#             song_serializer = SongSerializer(data={
#                                                 'name': song_data['trackName'],
#                                                 'artist': artist['id'],
#                                                 'album': album['id'],
#                                                 'release_date': song_data['releaseDate'],
#                                                 'genre_name': song_data['primaryGenreName'],
#                                                 'track_price': song_data['trackPrice'],
#                                                 'currency': song_data['currency'],
#                                                 'track_view_url': song_data['trackViewUrl'],
#                                                 'preview_url': song_data['previewUrl']
#                                             })
                                            
#             if song_serializer.is_valid():
#                 song_serializer.save()
#                 song_serializer = SongSerializer(song)
#             return song_serializer.data
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             print(song_data)
#             print(artist)
#             print(album)
#             return None
#     else:
#         song_serializer = SongSerializer(song)
#         return song_serializer.data
    





from rest_framework import status
import requests
import django
django.setup()


from music.models import Artist, Album, Song
from music.serializers import ArtistSerializer, AlbumSerializer, SongSerializer


class MusicSeeder:
    def __init__(self, artist_name):
        self.artist_name = artist_name

    def seed_data(self):
        """Seeds an artist's data from iTunes Search API (details, albums and songs)."""
        self.seed_music_data(self.artist_name)

    def seed_music_data(self, artist_name):
        url = 'https://itunes.apple.com/search'
        params = {'term': artist_name, 'entity': 'musicArtist'}
        response = requests.get(url, params=params)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            results = data.get('results', [])

            if results:
                # create artists object
                artist_data = results[0]
                artist = self._maybe_create_artist(artist_data['artistName'])

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
                            album = self._maybe_create_album(album_data, artist)

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
                                        self._maybe_create_song(song_data, artist, album)

    
    def _maybe_create_artist(self, name):
        artist =  Artist.objects.filter(name=name).first()
        if artist is None:
            artist_serializer = ArtistSerializer(data={
                'name': name
            })
            if artist_serializer.is_valid():
                artist = artist_serializer.save()
                artist_serializer = ArtistSerializer(artist)
            return artist_serializer.data
        else:
            artist_serializer = ArtistSerializer(artist)
            return artist_serializer.data

    
    def _maybe_create_album(self, album_data, artist):
        album =  Album.objects.filter(name=album_data['collectionName'], artist=artist['id']).first()

        if album is None:
            try:
                album_serializer = AlbumSerializer(data={
                    'name': album_data['collectionName'],
                    'artist': artist['id'],
                    'release_date': album_data['releaseDate'],
                    'genre_name': album_data['primaryGenreName'],
                    'collection_price': album_data['collectionPrice'],
                    'currency': album_data['currency'],
                    'artwork_url': album_data['artworkUrl100'],
                    'collection_view_url': album_data['collectionViewUrl']
                })
                if album_serializer.is_valid():
                    album = album_serializer.save()
                    album_serializer = AlbumSerializer(album)
                return album_serializer.data
            except Exception as e:
                print(f"An error occurred: {e}")
                print(album_data)
                return None

        else:
            album_serializer = AlbumSerializer
            return album_serializer.data

    
    def _maybe_create_song(self, song_data, artist, album):
        song = None
        try:
            song =  Song.objects.filter(name=song_data['trackName'], artist=artist['id'], album=album['id']).first()
        except Exception as e:
            print(f"An error occurred: {e}")
            print(song_data)
            print(artist)
            print(album)
            return None
        
        if song is None:
            try:
                song_serializer = SongSerializer(data={
                                                    'name': song_data['trackName'],
                                                    'artist': artist['id'],
                                                    'album': album['id'],
                                                    'release_date': song_data['releaseDate'],
                                                    'genre_name': song_data['primaryGenreName'],
                                                    'track_price': song_data['trackPrice'],
                                                    'currency': song_data['currency'],
                                                    'track_view_url': song_data['trackViewUrl'],
                                                    'preview_url': song_data['previewUrl']
                                                })
                                                
                if song_serializer.is_valid():
                    song_serializer.save()
                    song_serializer = SongSerializer(song)
                return song_serializer.data
            except Exception as e:
                print(f"An error occurred: {e}")
                print(song_data)
                print(artist)
                print(album)
                return None
        else:
            song_serializer = SongSerializer(song)
            return song_serializer.data
