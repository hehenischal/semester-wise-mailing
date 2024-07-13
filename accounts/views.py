from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def loginfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return render(request,'base.html')
        else:
            messages.warning(request,'Email or Password is incorrect')
            return render(request,'login.html')

    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'signup.html')

def error_404(request):
    return render(request,'404.html')

def base(request):
    return render(request,'base.html')