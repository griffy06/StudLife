from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="warden_login"),
    path('view/', views.logged_in, name="warden_logged_in"),
    path('view/<int:profile_id>', views.individual_request, name="warden_individual_request"),
]