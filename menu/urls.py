from django.urls import path
from . import views


urlpatterns = [
    path('menu', views.menu, name='menu'),
    path('menu/course/<int:course_id>/add', views.add_dish, name='add_dish'),
    path('menu/dish/<int:dish_id>/edit', views.edit_dish, name='edit_dish'),
    path('menu/dish/<int:dish_id>/delete', views.delete_dish,
         name='delete_dish'),
]
