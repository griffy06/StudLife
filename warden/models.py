from django.db import models


class Profile(models.Model):
    username = models.CharField(max_length=100, default=None)
    destination = models.CharField(max_length=100, default=None)
    vehicle = models.CharField(max_length=100, default=None)
    present_time = models.TimeField(default=None)
    arrival_time = models.TimeField(default=None)
    departure_time = models.TimeField(default=None)
    full_name = models.CharField(max_length=100, default=None)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Granted_outpasses(models.Model):
    username = models.CharField(max_length=100, default=None)
    destination = models.CharField(max_length=100, default=None)
    vehicle = models.CharField(max_length=100, default=None)
    present_time = models.TimeField(default=None)
    arrival_time = models.TimeField(default=None)
    departure_time = models.TimeField(default=None)
    full_name = models.CharField(max_length=100, default=None)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

