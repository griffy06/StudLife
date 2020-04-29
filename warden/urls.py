from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="warden_login"),
    path('view/', views.logged_in, name="warden_logged_in"),
    path('view/view_requests', views.view_requests, name='view_requests'),
    path('view/view_requests/<int:profile_id>', views.individual_request, name="warden_individual_request"),
    path('logout_warden/', views.warden_logout, name='warden_logout'),
    path('edit_profile_warden/', views.warden_edit_profile, name='warden_edit_profile')
]