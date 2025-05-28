from django.urls import path
from .views import home,logIn


urlpatterns = [
    path('',home, name='home'),
    path('logIn/',logIn,name='logIn')
]