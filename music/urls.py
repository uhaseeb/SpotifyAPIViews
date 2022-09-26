from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'),
    path('song/<int:id>', views.TrackDetailView.as_view(), name='song_detail'),
    path('favorite_track', views.FavoriteTrackDetailView.as_view(), name='favorite_track'),
    path('all_songs', views.AllTracksView.as_view(), name='all_songs'),
    path('album/<int:id>', views.AlbumDetailView.as_view(), name='album_detail'),
    path('artist/<int:id>', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('create_user', views.CreateUserView.as_view(), name='create_user'),
    path('login', views.LoginView.as_view(), name='login'),
    path('login_auth', views.LoginAuthView.as_view(), name='login_auth'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile_view', views.ProfileView.as_view(), name='profile_view'),
    path('detail_playlist/<str:name>', views.DetailPlaylistView.as_view(), name='detail_playlist'),
    path('create_playlist', views.CreatePlaylistView.as_view(), name='create_playlist')

]
