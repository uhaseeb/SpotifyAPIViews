from rest_framework import serializers
from music.models import Track, Album, Artist, Playlist, Genre
from users.models import User
from rest_framework import response
from rest_framework.validators import ValidationError

class TrackSerializer(serializers.ModelSerializer):
    artist = serializers.CharField(required=True)
    album = serializers.CharField(required=True)
    genre = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = Track

    # def create(self, validated_data):
    #     artist_data = validated_data.pop('artist')
    #     artist, _ = Artist.objects.get_or_create(name=artist_data)
    #     album_data = validated_data.pop('album')
    #     album, _ = Album.objects.get_or_create(name=album_data, defaults={"artist": artist})
    #     genre_data = validated_data.pop('genre')
    #     genre, _ = Genre.objects.get_or_create(name=genre_data)
    #     track = Track.objects.create(**validated_data, album=album, artist=artist)
    #     track.genre.add(genre)
    #     return track


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Artist


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['artist']
        model = Album


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=60, label='Username')
    password = serializers.CharField(max_length=30, label='Password', style={'input_type':'password'})


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=40, style={'input_type':'password'})
    confirm_password = serializers.CharField(max_length=40, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'gender']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({'message': 'Password doesnot matches'})
        return data

    def create(self, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        user.create_default_playlist()
        return user


class CreateTrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    artist = ArtistSerializer()
    genre = GenreSerializer()
    owner = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ['artist', 'album', 'genre', 'name', 'length', 'thumbnail', 'owner']
        model = Track

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        artist_data = validated_data.pop('artist')['name']
        artist, _ = Artist.objects.get_or_create(name=artist_data)
        album_data = validated_data.pop('album')['name']
        album, _ = Album.objects.get_or_create(name=album_data, defaults={'artist': artist})
        genre_data = validated_data.pop('genre')['name']
        genre, _ = Genre.objects.get_or_create(name=genre_data)
        track = Track.objects.create(**validated_data, album=album, artist=artist)
        track.genre.add(genre)
        return track


class TrackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Track

    def update(self, instance, validated_data):

        instance.save()
        return instance


class AlbumListSerializer(serializers.Serializer):
    artist = ArtistSerializer()
    # artist = serializers.CharField(read_only=True, source='artist.name')
    track_count = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = '__all__'

    def get_track_count(self, obj):
        return obj.tracks.all().count()


class AddRemoveFavoritesSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Track.objects.all())

    def create(self, validated_data):
        track = validated_data.get('id')
        request = self.context.get('request')
        liked_songs_playlist = request.user.playlists.get(name='liked_songs')
        if liked_songs_playlist.tracks.filter(id=track.id).exists():
            liked_songs_playlist.tracks.remove(track)
        else:
            liked_songs_playlist.tracks.add(track)

        return track


class AddRemovePlaylistSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Track.objects.all())
    name = serializers.CharField(max_length=40)

