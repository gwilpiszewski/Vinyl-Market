"""Projekt_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vinyl_market.views import RegisterUserView, MainView, LoginUserView, LogOutView, ArtistAddView, AlbumAddView, \
    GenreAddView, AlbumListView, ArtistUpdateView, UserOfferAddView, UserOfferPublicListView, \
    TrackAddView, AlbumUpdateView, AlbumAddManyArtists, AlbumDetailView, AboutView, \
    AlbumDeleteView, MessageSendView, MessageDeleteView, MessagesReceivedView, MessagesSentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main_view'),
    path('about/', AboutView.as_view(), name='about_view'),
    path('register_user/', RegisterUserView.as_view(), name='register_user_view'),
    path('login/', LoginUserView.as_view(), name='login_view'),
    path('logout/', LogOutView.as_view(), name='logout_view'),
    path('add_artist/', ArtistAddView.as_view(), name='add_artist_view'),
    path('update_artist/<int:pk>/', ArtistUpdateView.as_view(), name='artist_update_view'),
    path('add_album/', AlbumAddView.as_view(), name='add_album_view'),
    path('add_album_manyartists/', AlbumAddManyArtists.as_view(), name='add_album_many_artists'),
    path('delete_album/<int:pk>/', AlbumDeleteView.as_view(), name='delete_album_view'),
    path('add_genre/', GenreAddView.as_view(), name='add_genre_view'),
    path('album_list/', AlbumListView.as_view(), name='album_list_view'),
    path('album_details/<int:pk>/', AlbumDetailView.as_view(), name='album_detail_view'),
    path('add_album_to_market/<int:pk>/', UserOfferAddView.as_view(), name='album_add_to_market_view'),
    path('album_update/<int:pk>/', AlbumUpdateView.as_view(), name='album_update_view'),
    path('album_update/<int:pk>/add_track/', TrackAddView.as_view(), name='track_add_view'),
    path('user_offer_view/', UserOfferPublicListView.as_view(), name='user_offer_public_view'),
    path('messages/', MessagesReceivedView.as_view(), name='messages_view'),
    path('messages_sent/', MessagesSentView.as_view(), name='messages_sent'),
    path('send_message/<int:pk>/', MessageSendView.as_view(), name='sent_message'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='del_message'),



]
