from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants
from music.models import Playlist, Album, Artist, Track


class User(AbstractUser):
    gender = models.CharField(max_length=30, choices=constants.gender_choice, default='Male')

    def create_default_playlist(self):
        all_tracks = Track.objects.all()
        playlist = self.playlists.create(name=f"{self.username}_liked_songs")
        playlist.tracks.add(*all_tracks)
        return playlist



