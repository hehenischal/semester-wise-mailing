from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import Custom_user


def loginfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.warning(request,'Email or Password is incorrect',extra_tags="danger")
            return redirect('login')

    return render(request,'login.html')

@login_required
def logoutfunc(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        first_name = username.split(' ')[0]
        last_name = username.split(' ')[1]
        if password == password1:
            try:
                user = Custom_user.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password)
                user.save()
                messages.success(request,'User created successfully')
                return render(request,'login.html')
            except:
                messages.error(request, 'User creation failed; Maybe User already exists', extra_tags='danger')
                return render(request, 'signup.html')
        else:
            messages.warning(request,'Password does not match')
            return render(request,'signup.html')
        
    return render(request, 'signup.html')


def forgot_password(request):
    return render(request,'password_reset.html')

def error_404(request):
    return render(request,'404.html')

def base(request):
    return render(request,'base.html')
