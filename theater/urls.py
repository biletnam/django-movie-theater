from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show', views.show, name='theater-show'),
    url(r'^booked', views.booked, name='theater-booked'),
    url(r'^history', views.history, name='theater-history'),
    url(r'^logout/$', views.logout, name='logout'),
]
