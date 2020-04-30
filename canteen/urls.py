from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="canteen_login"),
    path('view/', views.logged_in, name="canteen_logged_in"),
    path('view/view_requests', views.view_requests, name='view_orders'),
    path('view/view_requests/<int:profile_id>', views.individual_request, name="canteen_individual_order"),
    path('logout_canteen/', views.canteen_logout, name='canteen_logout'),
    path('edit_profile_canteen/', views.canteen_edit_profile, name='canteen_edit_profile'),
    path('view/update_status/<int:profile_id>', views.update_status, name='update_status')
]