from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from .models import Profile, Granted_appointment

class UserFormView(View):

    template_name = 'doctor/doctor_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        userGroup = Group.objects.get(user=user).name
        if user is not None and userGroup == 'doctors':
            login(request, user)
            return redirect('doctor_logged_in')
        else:
            return render(request, self.template_name)


def logged_in(request):
    all_profiles = Profile.objects.all()
    return render(request, 'doctor/doctor_page.html', {'all_profiles': all_profiles})

def individual_request(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    user = User.objects.get(username=profile.username)
    if request.method == "GET":
        return render(request, 'doctor/individual_request.html', {'profile': profile})

    else:
        if request.POST.get('allow') == "confirm":
            granted_appointment = Granted_appointment()
            granted_appointment.username = profile.username
            granted_appointment.time = profile.time
            granted_appointment.date = profile.date
            granted_appointment.full_name = profile.full_name
            granted_appointment.save()
            user.student.appointments = 2
            user.save()
            profile.delete()
            return redirect('doctor_logged_in')
        else:
            user.student.appointments = 3
            user.save()
            profile.delete()
            return redirect('doctor_logged_in')

