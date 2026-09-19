from django.urls import path
from . import views


urlpatterns = [
    path('hours', views.opening_hours, name='hours'),
    path('delete_reservation/<int:id>', views.delete_reservation,
         name='delete_reservation'),
    path('reservations/<int:year>-<int:month>-<int:day>/'
         '<int:long_hour>:<int:minute>', views.reserve, name='reserve'),
    path('reservations/<int:year>-<int:month>-<int:day>',
         views.reservation_times, name='reservation_times'),
    path('reservations/admin',
         views.admin_calendar, name='admin_calendar'),
    path('reservations', views.reservations, name='reservations'),
]
