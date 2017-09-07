# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


# Create your models here.


class Repertoire(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class SeatTentative(models.Model):
    id = models.AutoField(primary_key=True)
    seat_id = models.PositiveIntegerField()
    repertoire_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def create(cls, seat_id, repertoire_id, user_id):
        model = cls(seat_id=seat_id, repertoire_id=repertoire_id, user_id=user_id)
        return model


class SeatBooked(models.Model):
    id = models.AutoField(primary_key=True)
    seat_id = models.PositiveIntegerField()
    repertoire_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    group = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @classmethod
    def create(cls, seat_id, movie_id, user_id, group):
        model = cls(seat_id=seat_id, repertoire_id=movie_id, user_id=user_id, group=group)
        return model

    def get_movie(cls):
        return Repertoire.objects.get(pk=cls.repertoire_id)