import pytest
from django.test import Client


# main
@pytest.mark.django_db
def test_main(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('')
    assert response.status_code == 200


# about
@pytest.mark.django_db
def test_about(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('/about/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register():
    c = Client()
    response = c.post('/register_user/', {
        'username': 'UserOne',
        'email': 'email@nostromo.com',
        'password': 'temporary_password'
    })
    assert response.status_code == 200


# login
@pytest.mark.django_db
def test_login(user):
    login_data = {
        'username': user.username,
        'password': "tymczasowe"
    }
    c = Client()
    response = c.post('/login/', login_data)
    assert response.status_code == 200


# logout
@pytest.mark.django_db
def test_logout(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('/logout/')
    assert response.status_code == 200


# add artist
@pytest.mark.django_db
def test_add_artist(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post('/add_artist/', {'name': 'Run the Jewels', 'bio': 'best current rap music!'})
    assert response.status_code == 302


# update artist
@pytest.mark.django_db
def test_update_artist(user, artist):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post(f'/update_artist/{artist.pk}/', {'artist': artist})
    assert response.status_code == 200


# add album
@pytest.mark.django_db
def test_add_album(user, artist, genre):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    album = {
        'title': "Run the Jewels 3",
        'label': "label",
        'country': "US",
        'released': 1234,
        'artist': artist,
        'user': user.username,
        'genre': genre.pk
    }
    response = c.post("/add_album/", album)
    assert response.status_code == 200


# album add many artists
@pytest.mark.django_db
def test_album_add_many_artists(user, genre, artist):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    album = {
        'title': "dupa maryny",
        'label': "label",
        'country': "US",
        'released': 1234,
        'artist': artist,
        'user': user.username,
        'genre': genre.pk
    }
    response = c.post("/add_album/", album)
    assert response.status_code == 200


# delete album
@pytest.mark.django_db
def test_delete_album(user, album):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post(f'/delete_album/{album.id}/')
    assert response.status_code == 302


# add genre
@pytest.mark.django_db
def test_add_genre(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post('/add_genre/', {'kind': 'progrock'})
    assert response.status_code == 200


# display album list
@pytest.mark.django_db
def test_album_list(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('/album_list/')
    assert response.status_code == 200


# album detailed view
@pytest.mark.django_db
def test_album_details_view(user, album):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get(f'/album_details/{album.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_album_to_market(user, album):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post(f'/add_album_to_market/{album.pk}', {'album': album, 'price': 10})
    assert response.status_code == 301


@pytest.mark.django_db
def test_update_album(user, album):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post(f'/album_update/{album.pk}/', {'album': album})
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_track(user, album):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post(f'/album_update/{album.pk}/add_track/', {'album': album, 'name': 'In War and Pieces'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_offer_view(user, album):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('/user_offer_view/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_messages(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('/messages/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_sent_messages(user):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.get('/messages_sent/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_message(user, message):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    response = c.post(f'/message_delete/{message.id}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_send_message(user, user2):
    c = Client()
    c.login(username=user.username, password="tymczasowe")
    message = {
        'receiver': user2.pk,
        'message': "Test message"
    }
    response = c.post(f'/send_message/{user2.pk}/', message)
    assert response.status_code == 302
