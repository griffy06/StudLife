from django.db import models


class Profile2(models.Model):
    username = models.CharField(max_length=100, default=None)
    full_name = models.CharField(max_length=100, default=None)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=None)

    def __str__(self):
        return self.username


class Granted_appointment(models.Model):
    username = models.CharField(max_length=100, default=None)
    full_name = models.CharField(max_length=100, default=None)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=None)

    def __str__(self):
        return self.username

