from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('login', login.as_view() , name="login"),
]