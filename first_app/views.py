from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from first_app.models import UserInfo
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# from first_app.forms import NewUser
from django.shortcuts import redirect
from .forms import NameForm


# Create your views here.
def index(request):
    return render(request, 'first_app/signin.html')


def users(request):
    user_list = User.objects.order_by('first_name')
    user_dict = {'users': user_list}
    return render(request, 'first_app/users.html', context=user_dict)


def register_user(request):
    message = "Please Sign up"
    f_name = request.GET.get('first_name')
    l_name = request.GET.get('last_name')
    username = request.GET.get('username')
    email = request.GET.get('email')
    password1 = request.GET.get('password1')
    password2 = request.GET.get('password2')
    print(email, password1)
    if email:
        try:
            if (
                    '@gmail.com' or '.com' or '.in' or '.co' or '@facebook.com' or '@grssl.uk' or '@grassrootsbpo.com' or '@yahoo.com') in email:
                if password1 == password2:
                    validate_email = User.objects.get(email=email)
                    if validate_email.email:
                        message = 'User with this email already exist.'
                    else:
                        message = 'Invalid login, Email or Password is incorrect.'
                else:
                    message = "Password doesn't matched"
            else:
                message = 'Invalid login, Email or Password is incorrect.'

        except ObjectDoesNotExist:
            try:
                if len(password1) < 6:
                    message = "password length must be greater than 6"

                elif (password1 and password2) is not None:
                    user = User.objects.create_user(username=username, email=email, password=password1,
                                                    first_name=f_name,
                                                    last_name=l_name)

                    UserInfo.objects.create(user=user)
                    return HttpResponseRedirect('/first_app/login/')
                else:
                    message = 'Invalid login, Email or Password is incorrect.'
            except IntegrityError:
                message = "Username already exists"
    return render(request, 'first_app/register.html', {'message': message})


def change_pass(request):
    message = "Change Password"
    if request.method == 'GET':
        email = request.GET.get('email')
        password1 = request.GET.get('password1')
        password2 = request.GET.get('password2')
        print(password1, password2)
        try:
            if password1 == password2:
                u = User.objects.get(email=email)
                u.set_password(password1)
                u.save()
                return HttpResponseRedirect('/first_app/login/', status=200)
            else:
                message = "Passwords doesn't Match"
        except ObjectDoesNotExist:
            message = "E-mail not matched"
    return render(request, 'first_app/change_password.html', {'message': message})


def login(request):
    message = "Please Sign In"
    if request.method == 'GET':
        user_name = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = User.objects.get(username=user_name)
            u_info = user.userinfo if hasattr(user, 'userinfo') else None
            invalid = False
            if u_info and u_info.last_invalid_time and u_info.invalid_login_attempts >= 3 and u_info.last_invalid_time.replace(tzinfo=None) + timedelta(minutes=30) > datetime.now():
                invalid = True
            if user.is_superuser:
                items = UserInfo.objects.all()
                info = details(request, user)
                print(info)
                if info[0] == 'edit':
                    a = items.get(id=info[1])
                    u_info = {'id': a.id, 'Name': a.name, 'salary': a.salary,
                              'contact': a.contact, 'designation': a.designation}
                    print(u_info)
                    return JsonResponse({'url': '/first_app/edit_details/{}'.format(a.id)}, status=200)
                return render(request, 'first_app/admin.html', context={'items': items})

            elif authenticate(username=user_name, password=password) and not invalid:
                    if hasattr(user, 'userinfo'):
                        u_info.invalid_login_attempts = 0
                        u_info.save()
                    return HttpResponseRedirect('/first_app/base/')
            else:
                u_info = user.userinfo
                u_info.invalid_login_attempts = u_info.invalid_login_attempts + 1
                u_info.last_invalid_time = datetime.now()
                u_info.save()
                message = 'Invalid login, Please try again.'

            if invalid:
                message = 'Too many attempts please try after 30 min'
        except ObjectDoesNotExist:
            message = 'Invalid login, Please try again.'
        except AttributeError:
            message = message
    return render(request, 'first_app/signin.html', {'message': message})


def details(request, user):
    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        print(id, action)

        if action == 'not_appr':
            u = UserInfo.objects.filter(id=id)
            u.delete()
            return True, ''

        if action == 'appr':
            u = UserInfo.objects.get(id=id)
            u.is_approved = True
            u.save()
            return True, ''

        if action == 'edit':
            u = UserInfo.objects.get(id=id)
            return 'edit', id
    return True, ''


def get_approval_pending_users(request):
    users = UserInfo.objects.filter(is_approved=None)
    return HttpResponse(users.count())


def base(request):
    message = 'Please Fill The Details'
    return render(request, 'first_app/base.html', {'message': message})


def admin(request):
    return render(request, 'first_app/admin.html')


def employee_detail(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        img = request.FILES["img"]
        designation = request.POST.get('designation')
        salary = request.POST.get('salary')
        contact = request.POST.get('contact')

        print(full_name, img, designation, salary)
        user = UserInfo.objects.create(name=full_name, profile_picture=img, salary=salary, contact=contact,
                                       designation=designation)
        user.save()
        # f = UserInfo(full_name=full_name)
        message = "Thanks, Your Application Has Been Submitted Successfully"
        return render(request, 'first_app/redirect_home.html', {'message': message})


def edit_details(request, *args, **kwargs):
    if request.method == 'POST':
        id = request.POST.get('id')
        full_name = request.POST.get('full_name')
        designation = request.POST.get('designation')
        salary = request.POST.get('salary')
        contact = request.POST.get('contact')

        user = UserInfo.objects.get(id=id)
        user.name = full_name
        user.salary = salary
        user.contact = contact
        user.designation = designation
        user.save()
        print(full_name, designation, salary)

        return HttpResponse("Thanks, Your Application Has Been Submitted Changed")
    else:
        user_id = kwargs.get('id')
        user = UserInfo.objects.get(id=user_id)
    return render(request, 'first_app/edit_details.html', {'user': user})
