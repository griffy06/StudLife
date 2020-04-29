from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="doctor_login"),
    path('view/', views.logged_in, name="doctor_logged_in"),
    path('view/<int:user_id>', views.show, name="show"),
    path('viewlist/<int:profile_id>/', views.individual_request, name="doctor_individual_request"),
]
