from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import TextComplaint,StatusTable,Category
from django.shortcuts import render
from django.shortcuts import render
from .models import AudioRecording
from .predictor import make_prediction 
from .predict import predict_from_speech
import re 

# @login_required(login_url='login')
import time
from datetime import datetime


def index(request):
    complains=TextComplaint.objects.all()
    recordings = AudioRecording.objects.all()
    
    context={
        'complains':complains,
        'recordings':recordings,
        'logged_in':request.user}
  
        
    return render(request,'index.html',context=context)

def complaint_table(request):
    complains=TextComplaint.objects.all()
    recordings = AudioRecording.objects.all()
    context={
        'complains':complains[max(0, len(complains) - 4):],
        'recordings':recordings[max(0, len(recordings) - 8):]}
  
    return render(request,'complaint_table.html',context=context)


def complain(request):

    if request.method=='POST':
    
        complain=request.POST['complaint']
        # province=request.POST['province']
        district=request.POST['district']
        # wardno=request.POST['ward']
        # municipality=request.POST['municipality']
        # criticality=request.POST['Criticality']
        #print(province,district,wardno,municipality,criticality)
        print(district)

        predicted_class = make_prediction(complain)


        # print(province,district,wardno,municipality)
        user=str(request.user)
       
        complaint_time=datetime.now()
        
      
        # text_complaint=TextComplaint(user=user,complaint=complain,complaint_time=complaint_time,province=province,district=district,wardno=wardno,municipality=municipality,predicted_class=predicted_class)
        text_complaint=TextComplaint(user=user,complaint=complain,complaint_time=complaint_time,predicted_class=predicted_class)

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
        print("inrecordaudio") 
        if request.method=="POST":
            print("post ma ayo")
            audio = request.FILES["audio"]
            text=predict_from_speech(audio)
            print(text)
            predicted_class = make_prediction(text)
            user=str(request.user)
            
            
            audio_file = AudioRecording.objects.create(
                                        title=predicted_class,
                                        user=user,
                                        audio_file=audio,
                                        converted_text=text
                                                                                )
            audio_path= audio_file.audio_file.path
            return render(request, "record.html", {"audio_path":audio_path})
        else:         
            print("Elsema")   
            return render(request, "record.html")

def audio_list(request):
    recordings = AudioRecording.objects.all()
    return render(request, 'audio_list.html', {'recordings': recordings})

def category(request):
    complains=TextComplaint.objects.all()
    category_name=Category.objects.all()
    print(category_name)
    context={
        'complains':complains,
        'category':category_name}
    
    return render(request,'category.html',context=context)



