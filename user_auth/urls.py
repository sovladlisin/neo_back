from django.urls import path
from django.conf.urls import url
from .views import login, register, setUserPermissions, getUsers

urlpatterns = [
    path('login',login , name='login'),
    path('register',register , name='register'),
    path('setUserPermissions',setUserPermissions , name='setUserPermissions'),
    path('getUsers',getUsers , name='getUsers'),
]