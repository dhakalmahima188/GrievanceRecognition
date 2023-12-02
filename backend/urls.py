
from django.urls import path
from .views import complain,login,index,record_audio,audio_list,complaint_table,category

urlpatterns=[

    path('',view=index,name='index'),
   path('complain',view=complain,name='complain'),
   path('login',view=login,name='login'),
    path('record/', view=record_audio, name='record_audio'),
     path('list/', audio_list, name='audio_list'),
     path('lists',view=complaint_table,name='complaint_table'),
       path('category',view=category,name='category')

    
]