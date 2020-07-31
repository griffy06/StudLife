from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile2, Granted_appointment
from django.contrib.auth.models import Group


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

class UserFormView(View):

    template_name = 'doctor/doctor_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            userGroup = Group.objects.get(user=user).name
            if user is not None and userGroup == 'doctors':
                login(request, user)
                return redirect('doctor_logged_in')
            else:
                return render(request, self.template_name)
        except Group.DoesNotExist:
            return render(request, self.template_name)

@login_required(login_url='doctor_login')
def logged_in(request):
    if has_group(request.user,"doctors")==False:
        return redirect('doctor_login')
    all_profiles = Profile2.objects.all()
    return render(request, 'doctor/doctor_dashboard.html', {'all_profiles': all_profiles})

@login_required(login_url='doctor_login')
def show(request):
    if has_group(request.user,"doctors")==False:
        return redirect('doctor_login')
    all_profiles = Profile2.objects.all()
    return render(request,'doctor/doctor_page.html', {'all_profiles': all_profiles})

@login_required(login_url='doctor_login')
def individual_request(request, profile_id):
    if has_group(request.user,"doctors")==False:
        return redirect('doctor_login')
    profile = Profile2.objects.get(pk=profile_id)
    user = User.objects.get(username=profile.username)
    if request.method == "GET":
        return render(request,'doctor/individual_request.html', {'profile': profile})

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
            return redirect('show')
        else:
            user.student.appointments = 3
            user.save()
            profile.delete()
            return redirect('show')

@login_required(login_url='doctor_login')
def doctor_logout(request):
    if has_group(request.user,"doctors")==False:
        return redirect('doctor_login')
    logout(request)
    return redirect('index')

@login_required(login_url='doctor_login')
def doctor_edit_profile(request):
    if has_group(request.user,"doctors")==False:
        return redirect('doctor_login')
    user = User.objects.get(username='executive.hc@iiita')
    if request.method == 'GET':
        return render(request, 'doctor/doctor_edit_profile.html', {'user': user})
    else:
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            user.save()
        if request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
            user.save()
        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
        if request.POST.get('password'):
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
        return redirect('doctor_logged_in')

@login_required(login_url='doctor_login')
def doctor_view_schedule(request):
    if has_group(request.user,"doctors")==False:
        return redirect('doctor_login')
    return render(request, 'doctor/schedule.html')