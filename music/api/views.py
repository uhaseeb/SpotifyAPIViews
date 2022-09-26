from music.models import Track, Album, Artist, Genre, Playlist
from users.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, exceptions
from rest_framework import generics
from .serializers import TrackSerializer, AlbumSerializer, ArtistSerializer, UserLoginSerializer,UserSignupSerializer, CreateTrackSerializer, TrackUpdateSerializer, AlbumListSerializer, AddRemoveFavoritesSerializer, AddRemovePlaylistSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import ValidationError


class IndexAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        search = request.query_params.get('search', '')

        track = Track.objects.filter(name__icontains=search)[:10]
        tracks = TrackSerializer(track, many=True)

        album = Album.objects.filter(name__icontains=search)[:10]
        albums = AlbumSerializer(album, many=True)

        artist = Artist.objects.filter(name__icontains=search)[:10]
        artists = ArtistSerializer(artist, many=True)

        context = {'tracks': tracks.data, 'album_serializer': albums.data,
                   'artists': artists.data}
        return Response(context)


class TrackDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackUpdateSerializer


class AlbumDetailAPIView(APIView):
    queryset = Album.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        album = Album.objects.get(id=pk)
        albums = AlbumSerializer(album)
        return Response(albums.data)


class ArtistDetailAPIView(APIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        artist = Artist.objects.get(id=pk)
        artists = ArtistSerializer(artist)
        return Response(artists.data)


class TracksListingAPIView(generics.ListAPIView):
    queryset = Track.objects.all().order_by('-id')
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['id']


class SignupAPIView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()


class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": user.username
            })


# class CreateTrackAPIView(generics.CreateAPIView):
#     serializer_class = TrackSerializer
#     queryset = Track.objects.all()
#     model = Track

class CreateTrackAPIView(generics.CreateAPIView):
    serializer_class = CreateTrackSerializer
    permission_classes = [IsAuthenticated]
    queryset = Track.objects.all()


class ArtistListAPIView(generics.ListAPIView):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()


class AlbumListAPIView(generics.ListAPIView):
    serializer_class = AlbumListSerializer
    queryset = Album.objects.all()


class FavoritesAPIView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = AddRemoveFavoritesSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def post(self, request, *args, **kwargs):
        fav_response = super().post(request, *args, **kwargs)
        liked_songs_playlist = request.user.playlists.get(name='liked_songs')
        liked_songs_tracks = liked_songs_playlist.tracks.all()
        track_serializer = TrackSerializer(liked_songs_tracks, many=True)
        context = {'track_serializer': track_serializer.data}
        return Response(context)

        # favorite_serializer = AddRemoveFavoritesSerializer(data=request.data)
        # favorite_serializer.is_valid(raise_exception=True)
        # track = favorite_serializer.validated_data['id']
        # track = get_object_or_404(Track, id=track_id)
        # if liked_songs_playlist.tracks.filter(id=track.id).exists():
        #     liked_songs_playlist.tracks.remove(track)
        # else:
        #     liked_songs_playlist.tracks.add(track)


class AddToPlaylistView(APIView):
    queryset = Track.objects.all()
    model = Track
    serializer_class = AddRemovePlaylistSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        playlist_serializer = AddRemovePlaylistSerializer(data=request.data)
        playlist_serializer.is_valid(raise_exception=True)
        track = playlist_serializer.validated_data['id']
        playlist_name = playlist_serializer.validated_data['name']
        if request.user.playlists.filter(name=playlist_name).exists():
            user_playlist = request.user.playlists.get(name=playlist_name)
            in_playlist = user_playlist.tracks.filter(name=track.name).exists()
            if not in_playlist:
                user_playlist.tracks.add(track)
            else:
                user_playlist.tracks.remove(track)
        else:
            raise ValidationError({"message": "Does not exist"})

        playlist_tracks = user_playlist.tracks.all()
        track_serializer = TrackSerializer(data=playlist_tracks, many=True)
        track_serializer.is_valid()
        return Response(track_serializer.data)



