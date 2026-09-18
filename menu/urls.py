from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('/admin', views.menu_admin, name='menu_admin'),
    path('/course/<int:course_id>/add', views.add_dish, name='add_dish'),
    path('/dish/<int:dish_id>/edit', views.edit_dish, name='edit_dish'),
    path('/dish/<int:dish_id>/delete', views.delete_dish,
         name='delete_dish'),
    path('/course/<int:course_id>/toggle', views.toggle_dishes,
         name='toggle_dishes'),
    path('/course/<int:course_id>/arrange', views.arrange_dishes,
         name='arrange_dishes'),
]
