from django.urls import path
from django.conf.urls import url
from .views import getClasses,getClassObjects, getSubClasses

urlpatterns = [
    path('getClasses',getClasses , name='getClasses'),
    path('getClassObjects',getClassObjects , name='getClassObjects'),
    path('getSubClasses',getSubClasses , name='getSubClasses'),
    
    ]