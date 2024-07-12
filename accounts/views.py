from django.shortcuts import render

# Create your views here.


def login(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'signup.html')

def error_404(request):
    return render(request,'404.html')

def base(request):
    return render(request,'base.html')