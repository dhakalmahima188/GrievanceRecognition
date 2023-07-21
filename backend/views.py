from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')

def index(request):
    return render(request,'homepage.html')

def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')    

