from django.urls import path
from django.conf.urls import url
from .views import (
    registration_view,
    login_view
)

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', login_view, name="login"),
]