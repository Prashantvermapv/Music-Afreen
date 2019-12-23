#from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q
from .models import Album,Song
from .forms import UserForm,SongForm,AlbumForm
#from django.core.mail import send_mail
#from django.conf import settings
#from django.views import generic
#from django.views.generic.edit import CreateView,UpdateView,DeleteView
#from django.views.generic import View
#from django.core.urlresolvers import reverse_lazy

AUDIO_FILE_TYPES=['wav','mp3','ogg']
IMAGE_FILE_TYPES=['png','jpg','jpeg']

def homeView(request):
    return render(request,'gaana/home.html')

def indexView(request):
    if not request.user.is_authenticated:
        return render(request,'gaana/login.html')
    else:
        all_album=Album.objects.filter(user=request.user)
        song_results=Song.objects.all()
        query=request.GET.get('q')
        if query:
            all_album=all_album.filter(Q(album_title__icontains=query) | Q(artist__icontains=query)).distinct()
            song_results=song_results.filter(Q(song_title__icontains=query)).distinct()
            return render(request,'gaana/index.html',{'all_album':all_album,'songs':song_results})
        else:
            return render(request,'gaana/index.html',{'all_album':all_album})


def detailView(request,album_id):
    if not request.user.is_authenticated:
        return render(request,'gaana/login.html')
    else:
        user=request.user
        album=get_object_or_404(Album,pk=album_id)                                  #work same as try except(
        return render(request,'gaana/detail.html',{'album':album,'user':user})      #try:
                                                                                    #album=Album.objects.get(pk=album_id)
                                                                                    #except Album.DoesNotExist:
                                                                                    #raise Http404('Does Not Exist'))
def albumCreate(request):
    if not request.user.is_authenticated:
        return render(request,'gaana/login.html')
    else:
        form=AlbumForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            album=form.save(commit=False)
            album.user=request.user
            album.album_logo=request.FILES['album_logo']
            file_type=album.album_logo.url.split('.')[-1]
            file_type=file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context={'album':album,'form':form,'error_message':'Image file must be PNG,JPG or JPEG'}
                return render(request,'gaana/create_album.html',context)
            else:
                album.save()
                return render(request,'gaana/detail.html',{'album':album})
        else:
            return render(request,'gaana/create_album.html',{'form':form})


def favouriteAlbum(request,album_id):
    album=get_object_or_404(Album,pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite=False
        else:
            album.is_favorite=True
        album.save()
    except (KeyError,album.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return JsonResponse({'success':True})


def song(request,filter_by):
    if not request.user.is_authenticated:
        return render(request,'gaana/login.html')
    else:
        try:
            song_ids=[]
            for album in Album.objects.filter(user=request.user):
                for songs in album.song_set.all():                          #remember: for songs in Album.song_set.all():
                    song_ids.append(songs.pk)
            user_songs=Song.objects.filter(pk__in=song_ids)
            if filter_by=='favorites':
                user_songs=user_songs.filter(is_favorite=True)              #not user_songs.objects.filter(is_favorite=True)
        except Album.DoesNotExist:
            user_songs=[]
        return render(request,'gaana/songs.html',{'song_list':user_songs,'filter_by':filter_by})


def songCreate(request,album_id):
    form=SongForm(request.POST or None, request.FILES or None)
    album=get_object_or_404(Album,pk=album_id)
    if form.is_valid():
        album_songs=album.song_set.all()
        for s in album_songs:
            if s.song_title==form.cleaned_data.get("song_title"):
                context={'album':album,'form':form,'error_message':'You already added that song'}
                return render(request,'gaana/create_song.html',context)
        song=form.save(commit=False)
        song.album=album
        song.audio_file=request.FILES['audio_file']
        file_type=song.audio_file.url.split('.')[-1]
        file_type=file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context={'album':album,'form':form,'error_message':'Audio file must be WAV,MP3,OGG'}
            return render(request,'gaana/create_song.html',context)
        song.save()
        return render(request,'gaana/detail.html',{'album':album})
    return render(request,'gaana/create_song.html',{'album':album,'form':form})
#need to sent from as model defined


def favouriteSong(request,song_id):
    song=get_object_or_404(Song,pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite=False
        else:
            song.is_favorite=True
        song.save()
    except(KeyError,song.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return JsonResponse({'success':True})

def lyrics(request,song_id):
    song=get_object_or_404(Song,pk=song_id)
    return render(request,'gaana/lyrics.html',{'song':song})

def deleteAlbum(request,album_id):
    album=Album.objects.get(pk=album_id)
    album.delete()
    all_album=Album.objects.filter(user=request.user)
    return render(request,'gaana/index.html',{'all_album':all_album})


def deleteSong(request,album_id,song_id):
    album=get_object_or_404(Album,pk=album_id)
    song=Song.objects.get(pk=song_id)
    song.delete()
    return render(request,'gaana/detail.html',{'album':album})


def register(request):
    form=UserForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user=authenticate(username=username,password=password)
        if user is not None:
                if user.is_active:
                    login(request,user)
                    all_album=Album.objects.filter(user=request.user)
                    return render(request,'gaana/index.html',{'all_album':all_album})
        return render(request,'gaana/register.html',{'form':form})
    else:
        return render(request,'gaana/register.html',{'form':form})

def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                all_album=Album.objects.filter(user=request.user)
                return render(request,'gaana/index.html',{'all_album':all_album})
            else:
                return render(request,'gaana/login.html',{'error_message':'Your account has been disabled'})
        else:
            return render(request, 'gaana/login.html', {'error_message': 'Invalid login'})
    return render(request, 'gaana/login.html')


def logout_user(request):
    logout(request)
    form=UserForm(request.POST or None)
    return render(request,'gaana/login.html',{'form':form})





'''
def index(request):
    all_album=Album.objects.all()
    context={'all_album':all_album}
    return render(request,'index.html',context)
class indexView(generic.ListView):
    template_name = 'gaana/index.html'
    content_object_name = 'all_albums' #otherwse ll take object name as all_objects not all_albums
    def query_set(self):
        return Album.objects.all()

class detailView(generic.DetailView):
    model=Album #specific to album with pk
    template_name = 'gaana/detail.html'

class AlbumCreate(CreateView):
    model=Album
    fields=['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model=Album
    fields=['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model=Album
    success_url=reverse_lazy('gaana:index')

class UserFormView(View):
    form_class=UserForm #blueprint we want
    template_name='gaana/registration_form.html'

    #display blank form
    def get(self,request):
        form=self.form_class(None)q
        return render(request,self.template_name,{'form': form})

    #process form data
    #all data get stored in request.POST and  django forms validate data issef(in forms.py)
    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commint=False)#just store data not in database

            #cleaned (normalized) data ie same formal eg date
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
'''
