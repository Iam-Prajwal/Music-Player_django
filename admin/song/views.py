from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from admin.genre.models import Genre
from admin.mood.models import Mood
from admin.artist.models import Artist
from admin.song.models import Song
import re
import random


# Create your views here.


# def random_song_id():
#     song_ids = Song.objects.values_list('id', flat=True)
#     if not song_ids:
#         return None
#     return random.choice(list(song_ids))

# @login_required(login_url='login')
# def index(request):
#     song_id = random_song_id()
#     if song_id is None:
#         # Handle the case when there are no songs
#         return redirect('no-songs')  # Create a template to handle no songs case
#     return redirect('player-index-id', sid=song_id)




@login_required(login_url='login')
def add(request):
    genre = Genre.objects.all()
    mood = Mood.objects.all()
    artist = Artist.objects.all()
    return render(request, 'adminTemplates/song/add.html', {'genre': genre, 'mood': mood, 'artist': artist})


@login_required(login_url='login')
def save(request):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        length = request.POST['length']
        mood_id = request.POST['mood']
        genre_id = request.POST['genre']
        artist_id = request.POST['artist']
        songFile = request.FILES['file']

        # Simplified regex patterns
        if not re.match(r'^[\w\s\-_.,]+$', name):
            messages.error(request, 'Enter a valid Song Name')
            return redirect('song-add')

        if not re.match(r'^[\w\s\-_.,!?]+$', desc):
            messages.error(request, 'Enter a valid Song Description')
            return redirect('song-add')

        if not re.match(r'^\d{2}:\d{2}$', length):
            messages.error(request, 'Enter a valid Song Length')
            return redirect('song-add')

        if songFile and not songFile.name.endswith(('.mp3', '.wav')):
            messages.error(request, 'Invalid File Type')
            return redirect('song-add')

        # Fetch related objects (ensure that they exist)
        try:
            genre = Genre.objects.get(pk=genre_id)
            artist = Artist.objects.get(pk=artist_id)
            mood = Mood.objects.get(pk=mood_id)
        except (Genre.DoesNotExist, Artist.DoesNotExist, Mood.DoesNotExist):
            messages.error(request, 'Invalid related data (Genre/Artist/Mood)')
            return redirect('song-add')

        # Create and save the song
        song = Song(
            song_name=name,
            song_des=desc,
            song_length=length,
            song_file=songFile,
            artist_name=artist,
            mood_name=mood,
            genre_name=genre
        )
        song.save()

        messages.success(request, 'Song Added Successfully!')
        return redirect('song-index')


@login_required(login_url='login')
def index(request):
    data = Song.objects.all()
    return render(request, 'adminTemplates/song/index.html', {'data': data})


@login_required(login_url='login')
def delete(request, id):
    if request.method == 'GET':
        try:
            song = Song.objects.get(pk=id)
            song.song_file.delete()  # Delete file from filesystem
            song.delete()  # Delete the record
            messages.success(request, 'Record Deleted!')
        except Song.DoesNotExist:
            messages.error(request, 'No such records found!')
        return redirect('song-index')


@login_required(login_url='login')
def edit(request, id):
    try:
        song = Song.objects.get(pk=id)
        genre = Genre.objects.all()
        mood = Mood.objects.all()
        artist = Artist.objects.all()
        return render(request, 'adminTemplates/song/edit.html', {'song': song, 'genre': genre, 'mood': mood, 'artist': artist})
    except Song.DoesNotExist:
        messages.error(request, 'No such records found!')
        return redirect('song-index')


@login_required(login_url='login')
def update(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        length = request.POST['length']
        mood_id = request.POST['mood']
        genre_id = request.POST['genre']
        artist_id = request.POST['artist']

        # Fetch related objects (ensure that they exist)
        try:
            artist = Artist.objects.get(pk=artist_id)
            genre = Genre.objects.get(pk=genre_id)
            mood = Mood.objects.get(pk=mood_id)
        except (Artist.DoesNotExist, Genre.DoesNotExist, Mood.DoesNotExist):
            messages.error(request, 'Invalid related data (Artist/Genre/Mood)')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Regex validation
        if not re.match(r'^[\w\s\-_.,]+$', name):
            messages.error(request, 'Enter a valid Song Name')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not re.match(r'^[\w\s\-_.,!?]+$', desc):
            messages.error(request, 'Enter a valid Song Description')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not re.match(r'^\d{2}:\d{2}$', length):
            messages.error(request, 'Enter a valid Song Length')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            song = Song.objects.get(pk=id)
        except Song.DoesNotExist:
            messages.error(request, 'No such records found!')
            return redirect('song-index')

        if 'file' in request.FILES:
            songFile = request.FILES['file']
            if not songFile.name.endswith(('.mp3', '.wav')):
                messages.error(request, 'Invalid File Type')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # Delete old file before saving new one
            song.song_file.delete()

            song.song_file = songFile

        song.song_name = name
        song.song_des = desc
        song.song_length = length
        song.artist_name = artist
        song.mood_name = mood
        song.genre_name = genre

        song.save()

        messages.success(request, 'Record Updated!')
        return redirect('song-index')


@login_required(login_url='login')
def details(request, id):
    try:
        song = Song.objects.get(pk=id)
        return render(request, 'adminTemplates/song/details.html', {'song': song})
    except Song.DoesNotExist:
        messages.error(request, 'No such records found!')
        return redirect('song-index')






