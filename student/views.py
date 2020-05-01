from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from warden.models import Profile, Granted_outpasses
from doctor.models import Profile2, Granted_appointment
from .render import Render
from .models import DocumentForm
from .models import Files, Order
from django.contrib.auth import logout
from canteen.models import Profile3
from canteen.models import Food_item
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class UserFormView(View):

    template_name = 'student/student_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        userGroup = Group.objects.get(user=user).name
        if user is not None and userGroup=='students':
            login(request, user)
            return redirect('logged_in', user.id)
        else:
            return render(request, self.template_name)


def logged_in(request,user_id):
    user = User.objects.get(pk=user_id)
    return render(request,'student/student_dashboard.html',{'user':user})


def outpass(request, user_id):
    if request.method == "GET":
        user = User.objects.get(pk=user_id)
        if user.student.outpass == 0:
            return render(request, 'student/outpass_page.html', {'user': user})
        elif user.student.outpass == 1:
            return render(request, 'student/outpass_requested_page.html', {'user': user})
        elif user.student.outpass == 2:
            return render(request, 'student/outpass_given_page.html', {'user': user})
        elif user.student.outpass == 3:
            return render(request, 'student/outpass_declined_page.html', {'user': user})

    else:
        user = User.objects.get(pk=user_id)
        user.student.outpass = 1
        user.save()
        profile = Profile()
        profile.username = user.username
        profile.destination = request.POST.get('destination')
        profile.vehicle = request.POST.get('vehicle')
        profile.present_time = request.POST.get('present_time')
        profile.arrival_time = request.POST.get('arrival_time')
        profile.departure_time = request.POST.get('departure_time')
        profile.date = request.POST.get('date')
        profile.full_name = request.POST.get('full_name')
        profile.save()
        return render(request, 'student/outpass_requested_page.html', {'user': user})




def view_menu(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'student/menu.html',{'user':user})


def fastfood(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request,'student/fastfood.html',{'user':user})


def fav(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request,'student/menu.html',{'user':user})


def maincourse(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request,'student/maincourse.html',{'user':user})


def refreshment(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request,'student/refreshments.html',{'user':user})

def hc(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'student/hc.html',{'user':user})

def digilocker(request, user_id):
    if request.method == 'POST':
        user=User.objects.get(pk=user_id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = Files(file=request.FILES['file'])
            new_file.username = user.username
            new_file.save()

            # Redirect to the document list after POST
            return redirect('digilocker', user_id)
    else:
        user=User.objects.get(pk=user_id)
        form = DocumentForm()  # A empty, unbound form

        # Load documents for the list page
    files = Files.objects.all()

    # Render list page with the documents and the form
    return render(request, 'student/digilocker_page.html', {'files': files, 'form': form, 'user' : user})


def back_outpass(request, user_id):
    user = User.objects.get(pk=user_id)
    user.student.outpass = 0
    user.save()
    try:
        permit = Granted_outpasses.objects.get(username=user.username)
        permit.delete()
        return redirect('outpass', user_id)
    except Granted_outpasses.DoesNotExist:
        return redirect('outpass', user_id)


def pdf(request,user_id):
    user = User.objects.get(pk=user_id)
    permit = Granted_outpasses.objects.get(username=user.username)
    go=permit.full_name
    params = {
        'full_name' : go,
        'going_to' : permit.destination,
        'vehicle': permit.vehicle,
        'date' : permit.date,
        'current_time': permit.present_time,
        'departure_time':permit.departure_time,
        'arrival_time': permit.arrival_time,
    }

    return Render.render('student/pdf.html', params)


def book_appointment(request, user_id):
    if request.method == "GET":
        user = User.objects.get(pk=user_id)
        if user.student.appointments == 0:
            return render(request, 'student/book_appointment_page.html', {'user': user})
        elif user.student.appointments == 1:
            return render(request, 'student/appointment_requested_page.html', {'user': user})
        elif user.student.appointments == 2:
            return render(request, 'student/appointment_booked_page.html', {'user': user})
        elif user.student.appointments == 3:
            return render(request, 'student/appointment_declined_page.html', {'user': user})

    else:
        user = User.objects.get(pk=user_id)
        user.student.appointments = 1
        user.save()
        profile = Profile2()
        profile.username = user.username
        profile.time = request.POST.get('time')
        profile.date = request.POST.get('date')
        profile.full_name = request.POST.get('full_name')
        profile.save()
        return render(request, 'student/appointment_requested_page.html', {'user': user})


def back_appointment(request, user_id):
    user = User.objects.get(pk=user_id)
    user.student.appointments = 0
    user.save()
    try:
        permit = Granted_appointment.objects.get(username=user.username)
        permit.delete()
        return redirect('book_appointment', user_id)
    except Granted_appointment.DoesNotExist:
        return redirect('book_appointment', user_id)


def view_schedule(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'student/schedule.html',{'user':user})

def pdf_appointment(request,user_id):
    user = User.objects.get(pk=user_id)
    permit = Granted_appointment.objects.get(username=user.username)
    params = {
        'username' : permit.username,
        'full_name' : permit.full_name,
        'date' : permit.date,
        'time': permit.time,
    }
    return Render.render('student/pdf_appointment.html', params)


def logout_student(request,user_id):
    logout(request)
    return redirect('index')





def order_food(request, user_id):
    user = User.objects.get(pk=user_id)
    try:
        profile = Profile3.objects.get(username=user.username)
        if profile.order_status == -1:
            return redirect('fav', user_id)
        elif profile.order_status == 0:
            return render(request, 'student/order_requested.html', {'user':user})
        elif profile.order_status == 1:
            return render(request, 'student/order_preparing.html', {'user':user})
        elif profile.order_status == 2:
            return render(request, 'student/order_cancelled.html', {'user':user})
        elif profile.order_status == 3:
            return render(request, 'student/order_prepared.html', {'user':user})
    except Profile3.DoesNotExist:
        return redirect('fav', user_id)


def add_food(request, user_id, food_id, val):
    user = User.objects.get(pk=user_id)
    try:
        order = Order.objects.get(food_id=food_id, username=user.username)
        order.quantity = order.quantity + 1
        order.save()
    except Order.DoesNotExist:
        try:
            profile = Profile3.objects.get(username=user.username)
        except Profile3.DoesNotExist:
            profile = Profile3()
            profile.username = user.username
            profile.order_status = -1
            profile.save()
        finally:
            order = Order()
            order.username=user.username
            order.food_id=food_id
            order.quantity=1
            order.save()
    finally:
        if val==1:
            return redirect('fav',user.id)
        elif val==2:
            return redirect('fast', user.id)
        elif val==3:
            return redirect('maincourse', user.id)
        else:
            return redirect('refreshment', user.id)


def remove_food(request, user_id, food_id, val):
    user = User.objects.get(pk=user_id)
    try:
        order = Order.objects.get(food_id=food_id, username=user.username)
        order.quantity = order.quantity - 1
        if order.quantity==0:
            order.delete()
        else:
            order.save()
        flag = 0;
        all_orders = Order.objects.all()
        for order in all_orders:
            if order.username==user.username:
                flag=1
                break
        if flag==0:
            obj = Profile3.objects.get(username=user.username)
            obj.delete()
    except Order.DoesNotExist:
        user=User.objects.get(pk=user_id)
    finally:
        if val == 1:
            return redirect('fav', user.id)
        elif val == 2:
            return redirect('fast', user.id)
        elif val == 3:
            return redirect('maincourse', user.id)
        else:
            return redirect('refreshment', user.id)


def back_order(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile3.objects.get(username=user.username)
    profile.delete()
    orders = Order.objects.all()
    for order in orders:
        if order.username == user.username:
            order.delete()
    return redirect('fav', user.id)


def cart(request, user_id):
    user = User.objects.get(pk=user_id)
    food = Order.objects.filter(username=user.username)
    food_item = Food_item.objects.all()
    if not food:
        return render(request, 'student/cart_empty.html', {'user':user})
    else:
        return render(request, 'student/cart.html', {'user':user, 'food':food, 'food_item':food_item})


def place_order(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile3.objects.get(username=user.username)
    profile.order_status=0
    profile.save()
    return render(request,'student/order_requested.html', {'user':user})


def student_edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'GET':
        return render(request, 'student/edit_profile_page.html', {'user': user})
    else:
        if request.POST.get('first_name'):
            user.first_name=request.POST.get('first_name')
            user.save()
        if request.POST.get('last_name'):
            user.last_name=request.POST.get('last_name')
            user.save()
        if request.POST.get('email'):
            user.email=request.POST.get('email')
            user.save()
        if request.POST.get('password'):
            password=request.POST.get('password')
            user.set_password(password)
            user.save()
        return redirect('logged_in', user_id)
