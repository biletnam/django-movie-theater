from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ping$', views.ping, name='rest-ping'),
    url(r'^tentative', views.tentative, name='rest-tentative'),
    url(r'^untentative', views.untentative, name='rest-untentative'),
    url(r'^book', views.book, name='rest-book'),
]
