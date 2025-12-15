from django.contrib import admin
from .models import BusStop, Route, Trip, StopEvent

admin.site.register(BusStop)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(StopEvent)
