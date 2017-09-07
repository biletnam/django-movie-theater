# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from rest.communicate import Communicate
from theater.models import SeatBooked, SeatTentative
from django.urls import reverse


# Create your views here.

def ping(request):
    movie_id = request.GET.get('movie_id')
    booked, tent = Communicate.gather_stats(movie_id)

    return JsonResponse({'tentative': tent, 'booked': booked})


def tentative(request):
    movie_id = request.GET.get('movie_id')
    for seat in request.GET.get('seat_id').split(','):
        seat = SeatTentative.create(seat, movie_id, request.user.id)
        seat.save()

    Communicate.tentative_push(movie_id)
    return HttpResponse(content_type="application/json", status=200)


def untentative(request):
    movie_id = request.GET.get('movie_id')
    for seat in request.GET.get('seat_id').split(','):
        SeatTentative.objects.filter(seat_id=seat, repertoire_id=movie_id, user_id=request.user.id).delete()

    Communicate.tentative_push(request.GET.get('movie_id'))
    return HttpResponse(content_type="application/json", status=200)


def book(request):
    movie_id = request.GET.get('movie_id')
    group = request.GET.get('group')
    for seat in request.GET.get('seat_id').split(','):
        seat = SeatBooked.create(seat, movie_id, request.user.id, group)
        seat.save()

    Communicate.tentative_push(movie_id)
    return JsonResponse({'redirect': reverse('theater-booked') + "?movie="+str(movie_id)+"&group="+group})
