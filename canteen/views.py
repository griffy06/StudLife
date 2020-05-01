from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from student.models import Order
from .models import Food_item, Profile3
from django.contrib.auth import logout


class UserFormView(View):

    template_name = 'canteen/canteen_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            userGroup = Group.objects.get(user=user).name
            if user is not None and userGroup == 'canteen_managers':
                login(request, user)
                return redirect('canteen_logged_in')
            else:
                return render(request, self.template_name)
        except Group.DoesNotExist:
            return render(request, self.template_name)


def logged_in(request):

    return render(request, 'canteen/canteen_dashboard.html')


def view_requests(request):
    all_profiles = Profile3.objects.all()
    return render(request,'canteen/canteen_page.html',{'all_profiles': all_profiles})


def individual_request(request, profile_id):
    profile = Profile3.objects.get(pk=profile_id)
    order = Order.objects.all()
    food_item = Food_item.objects.all()
    if request.method == "GET":
        return render(request, 'canteen/individual_request_page.html', {'profile': profile, 'order': order, 'food_item': food_item})

    else:
        profile = Profile3.objects.get(pk=profile_id)
        if request.POST.get('allow') == "confirm":
            profile.order_status=1
            profile.save()
            return redirect('view_orders')
        else:
            profile.order_status=2
            profile.save()
            return redirect('view_orders')


def update_status(request, profile_id):
    profile = Profile3.objects.get(pk=profile_id)
    order = Order.objects.all()
    food_item = Food_item.objects.all()
    if request.method=='GET':
        return render(request, 'canteen/update_status_page.html',{'profile':profile, 'order':order, 'food_item':food_item})
    else:
        profile.order_status = 3
        profile.save()
        return redirect('view_orders')


def canteen_logout(request):
    logout(request)
    return redirect('index')


def canteen_edit_profile(request):
    user = User.objects.get(username='canteen_manager@iiita')
    if request.method == 'GET':
        return render(request, 'canteen/canteen_edit_profile_page.html', {'user': user})
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
        return redirect('canteen_logged_in')



