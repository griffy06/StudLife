from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="doctor_login"),
]