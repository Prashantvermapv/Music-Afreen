from django import forms
from django.contrib.auth.models import User
from .models import Album,Song

class AlbumForm(forms.ModelForm):
    class Meta:
        model=Album
        fields=['artist','album_title','genre','album_logo']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_title', 'audio_file','lyrics']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    #so that form field dont show character instead show dots
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
