from django.urls import path
from . import views


urlpatterns = [
    path('menu', views.menu, name='menu'),
    path('menu/course/<int:course_id>/add', views.add_dish, name='add_dish'),
]
