from django.urls import path
from .views import home,signUp,logIn,main,logOut,create_candidate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home, name='home'),
    path('signUp/', signUp, name='signUp'),
    path('logIn/',logIn,name='logIn'),
    path('logOut/', logOut, name='logOut'),
    path('main/', main, name='main'),
    path('create_candidate/', create_candidate, name='create_candidate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)