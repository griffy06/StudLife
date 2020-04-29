from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.UserFormView.as_view(), name="student_login"),
    path('<int:user_id>/',views.logged_in, name="logged_in"),
    path('<int:user_id>/outpass/',views.outpass, name="outpass"),
    path('<int:user_id>/order_food/',views.order_food, name="order_food"),
    path('<int:user_id>/book_appointment/',views.book_appointment, name="book_appointment"),
    path('<int:user_id>/digilocker/',views.digilocker, name="digilocker"),
    path('<int:user_id>/outpass/back',views.back_outpass, name="back_outpass"),
    path('<int:user_id>/render/pdf',views.pdf, name="pdf"),
    path('<int:user_id>/book_appointment/back',views.back_appointment, name="back_appointment"),
    path('<int:user_id>/render/pdf_appointment',views.pdf_appointment, name="pdf_appointment"),
    path('<int:user_id>/logout_student', views.logout_student, name='logout_student'),
    path('<int:user_id>/edit_profile',views.student_edit_profile, name='student_edit_profile'),
    path('viewmenu/<int:user_id>',views.view_menu, name='view_menu'),
    path('viewmenu/<int:user_id>/fastfood',views.fastfood, name='fast'),
    path('viewmenu/<int:user_id>/fav', views.fav, name='fav'),
    path('viewmenu/<int:user_id>/refreshment', views.refreshment, name='refreshment'),
    path('viewmenu/<int:user_id>/maincourse', views.maincourse, name='maincourse'),
    path('hcSchedule/<int:user_id>', views.view_schedule, name='view_schedule'),

]
