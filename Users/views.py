from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CandidateForm, VoteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Candidates
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
import os
from django.contrib import messages
# Create your views here.


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
            messages.error(request, 'La contraseña o el correo electrónico son incorrectos.')
            return render(request,'users/logIn.html')
        user = authenticate(username=user.username, password=request.POST['password'])
        if user is None:
            messages.error(request, 'La contraseña o el correo electrónico son incorrectos.')
            return render(request,'users/logIn.html')
        if not user.is_active:
            messages.error(request, 'El usuario ya votó.')
            return render(request,'users/logIn.html')
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
            'candidates': Candidates.objects.all(),
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
    
    for vote in votes:
        if vote['user'] == request.user.username:
            return render(request, 'Users/main.html', {
                'ombudsmans': ombudsmans,
                'comptrollers': comptrollers,
                'error': 'Ya has votado.'
            })
    # Guardar información del voto en un archivo JSON
    voted_candidates = []
    for field in form.cleaned_data:
        candidate = form.cleaned_data[field]
        if hasattr(candidate, 'position'):
            voted_candidates.append({
                'candidate_id': candidate.id,
                'candidate_name': str(candidate),
                'position': candidate.position
            })
    vote_data = {
        'user': request.user.username,
        'voted_candidates': voted_candidates.user.username,
        'timestamp': timezone.now()
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