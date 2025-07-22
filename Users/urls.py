from django.urls import path
from .views import signUp,logIn,main,logOut,create_candidate,vote,results
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',logIn,name='logIn'),
    path('signUp/', signUp, name='signUp'),
    path('logOut/', logOut, name='logOut'),
    path('main/', main, name='main'),
    path('create_candidate/', create_candidate, name='create_candidate'),
    path('vote/',vote, name='votes'),
    path('results/',results,name='results')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)