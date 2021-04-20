from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from vinyl_market.models import User, Artist, Album, Genre, UserOffer, Message, Track
from vinyl_market.forms import LoginViewForm, RegisterUserForm, AlbumAddForm, \
    TrackAddForm, AlbumCreateForm, MessageForm, GenreAddForm


class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm
        return render(request, 'user_form.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        message2 = "User successfully registered. Please login using given credentials"
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
        return render(request, 'main.html', {'message2': message2})


class LoginUserView(View):
    def get(self, request):
        form = LoginViewForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginViewForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                message = "Login successful"
                return render(request, 'main.html', {'message2': message})
            else:
                message = "Invalid login, check your username and password"
                return render(request, 'login.html', {'message2': message, 'form': form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        message = "Logout successful"
        return render(request, 'logout.html', {'message2': message})


class ArtistAddView(LoginRequiredMixin, CreateView):
    model = Artist
    fields = ['name', 'bio']
    success_url = '/add_artist/'

    def get_context_data(self):
        context = super().get_context_data()
        context['artists'] = Artist.objects.all()
        return context


class AlbumAddView(LoginRequiredMixin, FormView):

    def get(self, request):
        form = AlbumAddForm()
        return render(request, 'album_form.html', {'form': form})

    def post(self, request, **kwargs):
        form = AlbumAddForm(request.POST)
        if form.is_valid():
            album = Album.objects.create(
                title=form.cleaned_data['title'],
                label=form.cleaned_data['label'],
                country=form.cleaned_data['country'],
                released=form.cleaned_data['released'],
                genre=form.cleaned_data['genre'],
                user=request.user
            )
            album.artist.add(form.cleaned_data['artist'])
            album.save()
            return redirect('album_list_view')
        else:
            return render(request, 'vinyl_market/album_list.html', {'form': form})


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = '/album_list/'


class AlbumListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)


class AlbumDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        album = Album.objects.get(pk=pk)
        return render(request, 'album_detail.html', {'album': album})


class AlbumAddManyArtists(LoginRequiredMixin, View):

    def get(self, request):
        user = self.request.user
        form = AlbumCreateForm(initial={'user': user})
        return render(request, 'album_many_artists_form.html', {'form': form})

    def post(self, request):
        form = AlbumCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            return redirect('album_list_view')


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['title', 'label', 'country', 'released', 'genre']
    template_name_suffix = '_update_form'
    success_url = '/album_list/'


class TrackAddView(LoginRequiredMixin, View):

    def get(self, request, pk):
        album = Album.objects.get(pk=pk)
        form = TrackAddForm()
        return render(request, 'track_add_template.html', {'form': form, 'album': album})

    def post(self, request, pk):
        titles = request.POST.getlist('name')
        if titles != "":
            for title in titles:
                Track.objects.create(name=title, album_id=pk)
            album = Album.objects.get(pk=pk)
            return render(request, 'album_detail.html', {'album': album})
        else:
            return render(request, 'main.html', {'message': "Error. Fill the form correctly"})


class ArtistUpdateView(LoginRequiredMixin, UpdateView):
    model = Artist
    fields = ['name', 'bio']
    template_name_suffix = '_update_form'
    success_url = '/add_artist/'


class GenreAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = GenreAddForm()
        genres = Genre.objects.all()
        return render(request, 'genre_form.html', {'form': form, 'genres': genres})

    def post(self, request):
        form = GenreAddForm(request.POST)
        genres = Genre.objects.all()

        if form.is_valid():
            kind = form.cleaned_data['kind']
            try:
                Genre.objects.get(kind=kind)
                return render(request, 'genre_form.html', {'form': form, 'genres': genres})
            except ObjectDoesNotExist:
                genre = Genre.objects.create(kind=kind)
                genre.save()
        return render(request, 'genre_form.html', {'form': form, 'genres': genres})


class UserOfferAddView(LoginRequiredMixin, View):
    def get(self, request, pk):
        album = Album.objects.get(pk=pk)
        return render(request, 'useroffer_form.html', {'album': album})

    def post(self, request, pk):
        user = request.user
        album = Album.objects.get(pk=pk)
        price = request.POST['price']
        if price != "":
            UserOffer.objects.create(
                user=user,
                album=album,
                price=price,
            )
            return redirect('user_offer_public_view')


class UserOfferPublicListView(ListView):
    model = UserOffer

    def get_queryset(self):
        return UserOffer.objects.all()


class MessagesReceivedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(receiver=user)
        return render(request, 'messages.html', {'messages': messages})


class MessagesSentView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        messages = Message.objects.filter(sender=user)
        return render(request, 'messages_sent.html', {'messages': messages})


class MessageSendView(LoginRequiredMixin, View):
    def get(self, request, pk):
        receiver = User.objects.get(pk=pk)
        form = MessageForm(initial={'receiver': receiver})
        return render(request, 'send_message.html', {'form': form})

    def post(self, request, pk):
        receiver = User.objects.get(pk=pk)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messages_sent')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = '/messages/'
