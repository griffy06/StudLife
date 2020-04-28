from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('developers', views.developers, name='developers'),
    path('student/', include('student.urls')),
    path('warden/', include('warden.urls')),
    path('doctor/', include('doctor.urls')),
    path('canteen/', include('canteen.urls')),
]