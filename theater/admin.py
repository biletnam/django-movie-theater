# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Repertoire, SeatBooked, Room


class RepertoireAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SeatBookedAdmin(admin.ModelAdmin):
    list_display = ('seat', 'user', 'movie', 'created_at', 'order')
    actions = None
    list_display_links = None

    def order(self, obj):
        return obj.group

    def movie(self, obj):
        return Repertoire.objects.get(pk=obj.repertoire_id).name

    def user(self, obj):
        user = User.objects.get(pk=obj.user_id)
        return "%s %s (%s)" % (user.first_name, user.last_name, user.username)

    def seat(self, obj):
        room = Room.objects.get(pk=obj.seat_id)
        return "seat = %d\n , row = %d\n" % (room.x, room.y)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Repertoire, RepertoireAdmin)
admin.site.register(SeatBooked, SeatBookedAdmin)
