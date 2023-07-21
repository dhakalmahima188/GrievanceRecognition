
from django.urls import path, include
from .views import index,login

urlpatterns=[

    
   path('',view=index,name='index'),
   path('login',view=login,name='login')
]