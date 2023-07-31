from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import TextComplaint
import time
from django.shortcuts import render
from django.http import JsonResponse
from .forms import AudioRecordingForm

from django.shortcuts import render
from .models import AudioRecording

# @login_required(login_url='login')



def index(request):
    complains=TextComplaint.objects.all()
    context={
        'complains':complains}
    print(complains)
    print(request.user)
        
    return render(request,'index.html',context=context)

def complaint_table(request):
    complains=TextComplaint.objects.all()
    recordings = AudioRecording.objects.all()
    context={
        'complains':complains,
        'recordings':recordings}
    print(complains)
    print(request.user)
        
    return render(request,'complaint_table.html',context=context)


def complain(request):
    print('ayo')
    if request.method=='POST':
        print('vitra aayo')
        complain=request.POST['complaint']
        user=request.user
        complaint_time=time.time()
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

# views.py


def record_audio(request):
    if request.method == 'POST':
        form = AudioRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = AudioRecordingForm()
    return render(request, 'record.html', {'form': form})

def audio_list(request):
    recordings = AudioRecording.objects.all()
    return render(request, 'audio_list.html', {'recordings': recordings})
