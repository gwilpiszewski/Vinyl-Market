from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)


class Artist(models.Model):
    name = models.CharField(max_length=128)
    bio = models.TextField(max_length=128)


class Album(models.Model):
    title = models.CharField(max_length=128)
    label = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    released = models.DateField()
    notes = models.TextField(max_length=1028)
    artist = models.ManyToManyField(Artist)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Track(models.Model):
    name = models.CharField(max_length=128)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)


class Genre(models.Model):
    kind = models.CharField(max_length=64, unique=True)


class UserOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    price = models.SmallIntegerField()


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)