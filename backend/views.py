from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import TextComplaint
from django.utils import timezone

# @login_required(login_url='login')



def index(request):
    complains=TextComplaint.objects.all()
    context={
        'complains':complains}
    print(complains)
    print(request.user)
        
    return render(request,'homepage.html',context=context)

def complain(request):
    print('ayo')
    if request.method=='POST':
        print('vitra aayo')
        complain=request.POST['complaint']
        user=request.user
        complaint_time=timezone.now()
        print(complain,user,complaint_time)
        text_complaint=TextComplaint(user=user,complaint=complain,complaint_time=complaint_time)
        text_complaint.save()       
        return redirect('/')
          
    
    return render(request,'complain.html')


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

