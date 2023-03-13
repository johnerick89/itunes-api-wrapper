from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

class Album(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateTimeField()
    genre_name = models.CharField(max_length=100, blank=False)
    collection_price =  models.FloatField(blank=True)
    currency = models.CharField(max_length=100)
    artwork_url =  models.CharField(max_length=255)
    collection_view_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


class Song(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    release_date = models.DateTimeField()
    genre_name = models.CharField(max_length=100)
    track_price = models.FloatField(blank=True)
    currency = models.CharField(max_length=100)
    track_view_url = models.CharField(max_length=255)
    preview_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
