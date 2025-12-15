from django.db import models

class BusStop(models.Model):
    stop_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"{self.stop_id} - {self.name}"

class Route(models.Model):
    route_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.route_id} - {self.name}"

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_date = models.DateField()

    def __str__(self):
        return f"Trip {self.id} ({self.route.route_id}) {self.service_date}"

class StopEvent(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    delay_seconds = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.trip} @ {self.stop.stop_id} ({self.arrival_time})"
