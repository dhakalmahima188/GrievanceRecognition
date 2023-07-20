
from django.urls import path, include
from .views import index

urlpatterns=[

    
   path('',view=index,name='index')
]