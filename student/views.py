from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


class UserFormView(View):

    template_name = 'student/student_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('logged_in', user.id)
        else:
            return render(request, self.template_name)


@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logged_in(request,user_id):

    user = User.objects.get(pk=user_id)
    return render(request,'student/student_page.html',{'user':user})


@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def outpass(request,user_id):

    return render(request,'student/outpass_page.html')


@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def book_appointment(request, user_id):
    return render(request, 'student/book_appointment_page.html')


@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_food(request, user_id):
    return render(request, 'student/order_food_page.html')


@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def digilocker(request, user_id):
    return render(request, 'student/digilocker_page.html')