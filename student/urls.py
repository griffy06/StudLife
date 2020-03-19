from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="student_login"),
    path('<int:user_id>/',views.logged_in, name="logged_in"),
    path('<int:user_id>/outpass/',views.outpass, name="outpass"),
    path('<int:user_id>/order_food/',views.order_food, name="order_food"),
    path('<int:user_id>/book_appointment/',views.book_appointment, name="book_appointment"),
    path('<int:user_id>/digilocker/',views.digilocker, name="digilocker"),
]