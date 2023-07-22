
from django.urls import path
from .views import complain,login,index

urlpatterns=[

    path('',view=index,name='index'),
   path('complain',view=complain,name='complain'),
   path('login',view=login,name='login'),
    
]