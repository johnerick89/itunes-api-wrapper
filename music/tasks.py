from celery import shared_task
from music.seed import MusicSeeder

@shared_task()
def seed_music_data_task(artist_name):
    """Seeds an artist's data from iTunes Search API (details, albums and songs)."""
    seeder = MusicSeeder(artist_name)
    seeder.seed_data()