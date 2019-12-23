from django.urls import path
from . import views
app_name='gaana'
urlpatterns = [
    path('',views.indexView,name='index'),
    path('detail/<int:album_id>/',views.detailView,name='detail'),
    path('album/add/',views.albumCreate,name='create_album'),
    path('album/favourite/<int:album_id>/',views.favouriteAlbum,name='album_favourite'),
    path('song/<str:filter_by>/',views.song,name='songs'),
    path('song/add/<int:album_id>',views.songCreate,name='create_song'),
    path('song/favourite/<int:song_id>/',views.favouriteSong,name='song_favourite'),
    path('album/<int:album_id>/delete_album/',views.deleteAlbum,name='delete_album'),
    path('song/<int:album_id>/delete_song/<int:song_id>/',views.deleteSong,name='delete_song'),
    path('register/',views.register,name='register'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('lyrics/<int:song_id>', views.lyrics,name='lyrics')
]
