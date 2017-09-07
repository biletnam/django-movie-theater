# Create your views here.
from pprint import pprint

from django.shortcuts import render, redirect, get_object_or_404
from theater.models import Repertoire, SeatBooked
from theater.models import Room
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def index(request):
    repertoire = Repertoire.objects.all()
    return render(request, 'theater/index.html', {'repertoire': repertoire})


@login_required
def show(request):
    movie = get_object_or_404(Repertoire, pk=request.GET.get('movie'))
    seats = Room.objects.order_by('y', 'x').all();
    return render(request, 'theater/show.html', {'seats': seats, 'movie': movie})


@login_required
def history(request):
    purchases = SeatBooked.objects.filter(user_id=request.user.id).order_by('created_at')
    from itertools import groupby


    schedule = dict()
    for k, v in groupby(purchases, lambda x: x.group):
        schedule[k] = list(v)

    return render(request, 'theater/history.html', {'purchases': purchases})


def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def booked(request):
    movie = get_object_or_404(Repertoire, pk=request.GET.get('movie'))
    seats = SeatBooked.objects.filter(user_id=request.user.id, repertoire_id=movie.id, group=request.GET.get('group'))
    return render(request, 'theater/booked.html', {'movie': movie, 'seats': seats})
