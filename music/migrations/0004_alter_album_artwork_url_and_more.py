# Generated by Django 4.1.7 on 2023-03-12 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0003_alter_album_release_date_alter_song_release_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="artwork_url",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="album",
            name="collection_view_url",
            field=models.CharField(max_length=255),
        ),
    ]