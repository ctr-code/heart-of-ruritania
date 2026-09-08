from django.contrib import admin
from .models import Reservation, Table, ServiceTime, ServiceException


admin.site.register(Reservation)
admin.site.register(Table)
admin.site.register(ServiceTime)
admin.site.register(ServiceException)
