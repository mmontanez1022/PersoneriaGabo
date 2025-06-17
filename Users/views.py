from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CandidateForm, VoteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Candidates
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
import os
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
        user = authenticate(username=user.username, password=request.POST['password'])
        if user is None:
            return render(request,'users/logIn.html',{
                'error' : 'La contraseña o el correo electrónico son incorrectos.'
            })
        if not user.is_active:
            return render(request,'users/logIn.html',{
                'error' : 'El usuario ya votó.'
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
    
@login_required(login_url='logIn')
def vote(request):
    ombudsmans = Candidates.objects.filter(position='Personería')
    comptrollers = Candidates.objects.filter(position='Contraloría')
    form = VoteForm(request.POST)
    try:
        candidate = Candidates.objects.get(id=request.POST.get('candidate'))
    except Candidates.DoesNotExist:
        candidate = None
    if not form.is_valid():
        return render(request,'Users/main.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })
    # Buscar si el usuario ya votó por un candidato
    votes_file = os.path.join(os.path.dirname(__file__), 'votes.json')
    try:
        with open(votes_file, 'r', encoding='utf-8') as f:
            votes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        votes = []
    # Verificar si el usuario ya ha votado
    for vote in votes:
        if vote['user'] == request.user.username:
            if vote['candidate'] == candidate.position:
                return render(request,'Users/main.html',{
                     'ombudsmans' : ombudsmans,
                    'comptrollers' : comptrollers,
                    'error' : f'Ya ha votado por {candidate.position}'
                })
    # Guardar información del voto en un archivo JSON
    vote_data = {
        'user': request.user.username,
        'candidate': candidate.position if candidate else None,
        'timestamp': timezone.now().isoformat(),
    }
    
    try:
        with open(votes_file, 'r', encoding='utf-8') as f:
            votes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        votes = []
    votes.append(vote_data)
    with open(votes_file, 'w', encoding='utf-8') as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)
    form.save(request.user)
    return redirect('main')

@login_required(login_url='logIn')
def results(request):
    ombudsmans = Candidates.objects.filter(position='Personería')
    comptrollers = Candidates.objects.filter(position='Contraloría') 
    return render(request,'Users/results.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })