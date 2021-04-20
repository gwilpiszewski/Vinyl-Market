import pytest
from vinyl_market.models import User, Genre, Artist, Album, Message


@pytest.fixture
def user():
    user = User.objects.create_user(pk=12, username='testowy', email='email@email.com', password='tymczasowe')
    return user


@pytest.fixture
def user2():
    user2 = User.objects.create_user(pk=13, username='testowy2', email='email2@email.com', password='tymczasowe2')
    return user2


@pytest.fixture
def genre():
    genre = Genre.objects.create(kind="funky")
    return genre


@pytest.fixture
def artist():
    artist = Artist.objects.create(name="Pentagram", bio="First doom metal band")
    return artist


@pytest.fixture
def album(artist, genre, user):
    album = Album.objects.create(
        pk=666,
        title="Heartwork",
        label="Reps",
        country="US",
        released='1994',
        genre=genre,
        user=user
    )
    artist.album_set.add()
    return album


@pytest.fixture
def message(user, user2):
    message = Message.objects.create(
        id=12,
        receiver=user2,
        sender=user,
        message="Test message"
    )
    return message
