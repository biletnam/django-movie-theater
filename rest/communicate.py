# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pusher

from theater.models import SeatTentative, SeatBooked
from django.conf import settings


class Communicate:
    @classmethod
    def push(self, event, data):
        pusher_client = pusher.Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=True
        )

        print(pusher_client.trigger('theater', event, data))

    @classmethod
    def tentative_push(cls, movie_id):
        booked, tent = cls.gather_stats(movie_id)
        Communicate.push('seatupdates_' + movie_id, {'tentative': tent, 'booked': booked})

    @classmethod
    def gather_stats(cls, movie_id):
        tent = []
        for seat in SeatTentative.objects.filter(repertoire_id=movie_id):
            tent.append(seat.seat_id)
        for seat in SeatBooked.objects.filter(repertoire_id=movie_id, confirmed=False):
            tent.append(seat.seat_id)
        booked = []
        for seat in SeatBooked.objects.filter(repertoire_id=movie_id, confirmed=True):
            booked.append(seat.seat_id)
        return booked, tent
