from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from .models import Profile, Granted_outpasses
from django.contrib.auth import logout


class UserFormView(View):

    template_name = 'warden/warden_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            userGroup = Group.objects.get(user=user).name
            if user is not None and userGroup == 'wardens':
                login(request, user)
                return redirect('warden_logged_in')
            else:
                return render(request, self.template_name)
        except Group.DoesNotExist:
            return render(request, self.template_name)


def logged_in(request):

    return render(request, 'warden/warden_dashboard.html')


def view_requests(request):
    all_profiles = Profile.objects.all()
    return render(request,'warden/warden_page.html',{'all_profiles': all_profiles})


def individual_request(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    user = User.objects.get(username=profile.username)
    if request.method == "GET":

        return render(request, 'warden/individual_request_page.html', {'profile': profile})

    else:
        if request.POST.get('allow') == "confirm":
            granted_outpass = Granted_outpasses()
            granted_outpass.username = profile.username
            granted_outpass.destination = profile.destination
            granted_outpass.vehicle = profile.vehicle
            granted_outpass.present_time = profile.present_time
            granted_outpass.arrival_time = profile.arrival_time
            granted_outpass.departure_time = profile.departure_time
            granted_outpass.date = profile.date
            granted_outpass.full_name = profile.full_name
            granted_outpass.save()
            user.student.outpass = 2
            user.save()
            profile.delete()
            return redirect('view_requests')
        else:
            user.student.outpass = 3
            user.save()
            profile.delete()
            return redirect('view_requests')


def warden_logout(request):
    logout(request)
    return redirect('index')


def warden_edit_profile(request):
    user = User.objects.get(username='warden@iiita')
    if request.method == 'GET':
        return render(request, 'warden/warden_edit_profile_page.html', {'user': user})
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
        return redirect('warden_logged_in')

