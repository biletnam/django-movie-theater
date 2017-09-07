from celery import task
from theater.models import SeatTentative, SeatBooked
from datetime import datetime, timedelta
from rest.communicate import Communicate


@task()
def trim_tentative():
    elements = SeatTentative.objects.filter(created_at__lte=(datetime.now() - timedelta(minutes=3)))
    movie_ids = elements.values_list('repertoire_id', flat=True).distinct()
    elements.delete()

    for movie_id in movie_ids:
        Communicate.tentative_push(str(movie_id))


@task()
def confirm_payments():
    toconfirm = SeatBooked.objects.filter(created_at__lte=(datetime.now() - timedelta(minutes=2)), confirmed=False)
    movie_ids = toconfirm.values_list('repertoire_id', flat=True).distinct()

    for seat in toconfirm:
        seat.confirmed = True
        seat.save()
        SeatTentative.objects.filter(repertoire_id=seat.repertoire_id, seat_id=seat.id).delete()

    for movie_id in movie_ids:
        Communicate.tentative_push(str(movie_id))
