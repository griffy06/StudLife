from django.db import models


class Food_item(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(default=None, primary_key=True)
    price = models.IntegerField(default=None)


class Profile3(models.Model):
    username = models.CharField(max_length=100)
    order_status = models.IntegerField(default=None)
