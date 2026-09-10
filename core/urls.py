from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hours', views.opening_hours, name='hours'),
    path('reservations/<int:year>-<int:month>-<int:day>',
         views.reservation_times, name='reservation_times'),
    path('reservations', views.reservations, name='reservations'),
]
