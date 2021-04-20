from datetime import datetime

import django.forms as forms
from django.forms import ModelForm

from vinyl_market.models import Artist, Genre, Album, Track, Message


class LoginViewForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterUserForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class EditUserForm:
    username = forms.CharField(label="New Username")
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class AlbumAddForm(forms.Form):
    title = forms.CharField(max_length=128)
    label = forms.CharField(max_length=128, required=False)
    country = forms.CharField(max_length=128, required=False)
    released = forms.IntegerField()
    artist = forms.ModelChoiceField(queryset=Artist.objects.all())
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'artist': forms.SelectMultiple()
        }


class TrackAddForm(forms.Form):
    name = forms.CharField(max_length=128)
    album = forms.CharField(max_length=128, widget=forms.HiddenInput())


class GenreAddForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['kind']


class UserOfferForm(forms.Form):
    user = forms.CharField(max_length=64)
    album = forms.CharField(max_length=128)
    price = forms.IntegerField()


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']

