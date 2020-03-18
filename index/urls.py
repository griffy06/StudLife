from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('student/', include('student.urls')),
    path('warden/', include('warden.urls')),
    path('doctor/', include('doctor.urls')),
    path('canteen/', include('canteen.urls')),
]