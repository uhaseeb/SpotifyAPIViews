from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('homepage', views.IndexAPIView.as_view(), name='index_page'),
    path('track_detail/<int:pk>', views.TrackDetailAPIView.as_view(), name='track_detail'),
    path('album_detail/<int:pk>', views.AlbumDetailAPIView.as_view(), name='album_detail'),
    path('artist_detail/<int:pk>', views.ArtistDetailAPIView.as_view(), name='artist_detail'),
    path('all_tracks', views.TracksListingAPIView.as_view(), name='all_tracks'),
    path('login', views.LoginAPIView.as_view(), name='login'),
    path('signup', views.SignupAPIView.as_view(), name='signup'),
    path('create_track', views.CreateTrackAPIView.as_view(), name='create_track'),
    path('all_album', views.AlbumListAPIView.as_view(), name='list_album'),
    path('all_artist', views.ArtistListAPIView.as_view(), name='list_artist'),
    path('favorite_track', views.FavoritesAPIView.as_view(), name='favorite_track'),
    path('add_to_playlist', views.AddToPlaylistView.as_view(), name='add_to_playlist'),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]
