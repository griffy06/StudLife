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
from .models import Files
from django.contrib.auth import logout


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


def order_food(request, user_id):
    return render(request, 'student/order_food_page.html')


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
    permit = Granted_outpasses.objects.get(username=user.username)
    permit.delete()
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
    permit = Granted_appointment.objects.get(username=user.username)
    permit.delete()
    return redirect('book_appointment', user_id)


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


def student_edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'student/edit_profile_page.html', {'user': user})
