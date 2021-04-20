from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=128)


class Artist(models.Model):
    name = models.CharField(max_length=128)
    bio = models.TextField(max_length=1024, blank=True)

    def __str__(self):
        return f"{self.name}"


class Genre(models.Model):
    kind = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.kind}"


class Album(models.Model):
    title = models.CharField(max_length=128)
    label = models.CharField(max_length=128)
    country = models.CharField(max_length=128, blank=True)
    released = models.IntegerField(blank=True)
    artist = models.ManyToManyField(Artist)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Track(models.Model):
    name = models.CharField(max_length=128)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)


class UserOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    price = models.SmallIntegerField()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
