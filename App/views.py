from django.shortcuts import render, redirect
from App.models import RegisterUser
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
import datetime
# from Password_Expiry.settings import PASSWORD_RESET_TIMEOUT_MINUTES

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        mobile = request.POST['mobile']
        email = request.POST['email']
        uname = request.POST['uname']
        pwd = request.POST['pwd']

        if User.objects.filter(email=email).exists():
            messages.error(request,'Email  Already exists.!')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.error(request,'Username Already Taken.!')
            return redirect('register')
        elif RegisterUser.objects.filter(mobile=mobile).exists():
            messages.error(request,'Mobile number Already Exists.!')
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=uname, password=pwd)
            user.save()

            reg_user = RegisterUser(user=user, mobile=mobile)
            reg_user.password_expiry = datetime.datetime.now() + timedelta(minutes=2)

            reg_user.save()
            return redirect('/')
        
    return render(request, 'register.html',{'message':messages})

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            if user.is_active:
                u = RegisterUser.objects.get(user=user.id)
                e = u.password_expiry
                e_t = e.strftime("%M:%S")
                now = datetime.datetime.now()
                c_t = now.strftime('%M:%S')
                if e_t < c_t:
                    messages.error(request, 'Password expired.!')
                    return redirect('login')
                else:
                    auth.login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'this account is disabled. please contact admin.')
                return redirect('login')
        else:
            messages.error(request, 'invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html',{'message':messages})
  
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('login')

