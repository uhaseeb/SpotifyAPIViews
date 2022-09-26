from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from .forms import SearchForm, CreatePlaylistForm
from users.forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Track, Playlist, Album, Artist
from users.models import User


class IndexView(LoginRequiredMixin, View):
    template_name = 'index.html'
    form = SearchForm

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            songs = Track.objects.filter(name__icontains=search)
            albums = Album.objects.filter(name__icontains=search)
            artists = Artist.objects.filter(name__icontains=search)
            context = {'artists': artists, 'songs': songs, 'albums': albums, 'form': form}
            return render(request, 'index.html', context)

    def get(self, request):
        form = SearchForm()
        return render(request, 'index.html', {'form': form})


class TrackDetailView(View):

    def get(self, request, id):
        all_playlist = request.user.playlists.all()
        track = Track.objects.get(id=id)
        liked_songs = request.user.playlists.get(name='liked_songs')
        is_favorite = liked_songs.track.filter(id=id).exists()
        context = {'track': track, 'all_playlist': all_playlist, 'is_favorite': is_favorite}
        return render(request, 'song_detail.html', context)

    def post(self, request, id):
        playlist_id = request.POST['selected_playlist']
        playlist = Playlist.objects.get(id=playlist_id)
        song = Track.objects.get(id=id)
        playlist.track.add(song)
        path = reverse('detail_playlist', args=[playlist.name])
        return HttpResponseRedirect(path)


class FavoriteTrackDetailView(View):
    def post(self, request):
        track_id = request.POST['track_id']
        liked_songs = request.user.playlists.get(name='liked_songs')
        track = Track.objects.get(id=track_id)
        is_favorite = liked_songs.track.filter(id=track_id).exists()
        if is_favorite:
            liked_songs.track.remove(track)
        else:
            liked_songs.track.add(track)
        path = reverse('song_detail', args=[track_id])
        return HttpResponseRedirect(path)


class AllTracksView(ListView):
    model = Track
    template_name = 'all_songs.html'
    context_object_name = 'all_songs'


class AlbumDetailView(View):
    def get(self, request, id):
        album = Album.objects.get(id=id)
        all_tracks = album.tracks.all()
        context = {'album': album, 'all_tracks': all_tracks}
        return render(request, 'album_detail.html', context)


class ArtistDetailView(View):
    def get(self, request, id):
        artist = Artist.objects.get(id=id)
        all_albums = artist.albums.all()
        context = {'artist': artist, 'all_albums': all_albums}
        return render(request, 'artist_detail.html', context)


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'signup.html'


class CreateUserView(View):
    model = User
    form_class = SignupForm

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']

            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return HttpResponseRedirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return HttpResponseRedirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, gender=gender)
                user.save()
                user.playlists.create(name='liked_songs')
                return HttpResponseRedirect('/music')

        return render(request, 'signup.html', {'form': form})

    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})


class LoginView(CreateView):
    template_name = 'login.html'
    model = User
    fields = ['username', 'password']


class LoginAuthView(View):
    model = User
    form_class = LoginForm
    template_name = 'login.html'

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/music')

        else:
            messages.info(request, "user credentials invalid")
            return HttpResponseRedirect('login')

    def get(self, request):
        form = LoginForm()

        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('login')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        all_playlists = user.playlists.all()
        context = {'user': user, 'all_playlists': all_playlists}
        return render(request, 'user_detail.html', context)


class DetailPlaylistView(View):
    def get(self, request, name):
        playlist = request.user.playlists.get(name=name)
        all_tracks = playlist.track.all()
        context = {'playlist': playlist, 'all_tracks': all_tracks}
        return render(request, 'playlist_detail.html', context)


class CreatePlaylistView(View):
    def post(self, request):
        form = CreatePlaylistForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            request.user.playlists.create(name=name)
            return HttpResponseRedirect('profile_view')
        else:
            return render(request, 'create_playlist.html', {'form': form})

    def get(self, request):
        form = CreatePlaylistForm()
        return render(request, 'create_playlist.html', {'form': form})




