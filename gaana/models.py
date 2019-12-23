from django.db import models
from django.contrib.auth.models import Permission,User

# Create your models here.
class Album(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    artist=models.CharField(max_length=100)
    album_title=models.CharField(max_length=200)
    genre=models.CharField(max_length=100)
    album_logo=models.FileField()
    is_favorite=models.BooleanField(default=False)
    def __str__(self):
        return self.album_title+'-'+self.artist

class Song(models.Model):
    album=models.ForeignKey(Album,on_delete=models.CASCADE)
    song_title=models.CharField(max_length=100)
    audio_file=models.FileField(default='')
    is_favorite=models.BooleanField(default=False)
    lyrics=models.TextField(max_length=50000, default='')
    def __str__(self):
        return self.song_title
