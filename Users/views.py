from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CandidateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Candidates
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'users/home.html')

@login_required(login_url='logIn')
def signUp(request):
    if not request.user.is_superuser:
        logout(request)
        return redirect('main')
    if request.method == 'GET':
        return render(request,'users/signUp.html',{
            'form': UserRegisterForm()
        })
    else:
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request,'users/signUp.html',{
                'form': form
            })
        user = form.save()
        return redirect('main')

def logIn(request):
    if request.method == 'GET':
        return render(request,'users/logIn.html')   
    else:
        try:
            user = User.objects.get(email=request.POST['email'])
        except User.DoesNotExist:
            return render(request,'users/logIn.html',{
                'error' : 'La contraseña o el correo electrónico son incorrectos.'
            })
        user = authenticate(username=user.username, password=request.POST['password'],is_active=True)
        if user is None:
            return render(request,'users/logIn.html',{
                'error' : 'La contraseña o el correo electrónico son incorrectos.'
            })
        login(request, user)
        return redirect('main')

def logOut(request):
    logout(request)
    return redirect('home')

@login_required(login_url='logIn')
def main(request):
    ombudsmans = Candidates.objects.filter(position='Personería')
    comptrollers = Candidates.objects.filter(position='Contraloría')
    if request.method == 'GET':
        return render(request,'users/main.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })
    else:
        return render(request,'users/main.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })

@login_required(login_url='logIn')
def create_candidate(request):
    if not request.user.is_superuser:
        logout(request)
        return redirect('main')
    users = User.objects.filter(is_active=True)
    candidates = Candidates.objects.all()
    if request.method == 'GET':
        return render(request,'users/create_candidate.html',{
            'form': CandidateForm(),
            'users': users,
            'candidates' : candidates
        })
    else:
        form = CandidateForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request,'users/create_candidate.html',{
                'form': form,
                'users': users,
                'candidates' : candidates
            })
        form.save()
        return redirect('main')