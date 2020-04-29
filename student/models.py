from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    outpass = models.IntegerField(default=0)
    appointments = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_student(sender, instance, **kwargs):
    instance.student.save()


class Files(models.Model):
    username = models.CharField(max_length=100, default=None)
    file = models.FileField()


@receiver(post_save, sender=User)
def create_user_files(sender, instance, created, **kwargs):
    if created:
        Files.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_files(sender, instance, **kwargs):
    instance.files.save()


class DocumentForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )