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
        messages.error(request, 'No tienes permiso para crear usuarios.')
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
    return redirect('logIn')

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
        messages.error(request, 'No tienes permiso para crear candidatos.')
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
    #Verifica que solo se manden datos por POST
    if request.method != 'POST':
        return redirect('main')
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'No tienes permiso para votar.')
        return redirect('main')
    form = VoteForm(request.POST)
    try:
        candidate = Candidates.objects.get(id=request.POST.get('candidate'))
    except Candidates.DoesNotExist:
        candidate = None
    if not form.is_valid():
        messages.error(request, 'Hubo un error al votar.')
        return redirect('main')
    # Buscar si el usuario ya votó por un candidato
    votes_file = os.path.join(os.path.dirname(__file__), 'votes.json')
    try:
        with open(votes_file, 'r', encoding='utf-8') as f:
            votes = json.load(f)
            print(votes)
    except (FileNotFoundError, json.JSONDecodeError):
        votes = []
    # Verificar si el usuario ya ha votado
    for vote in votes:
        if vote['user'] == request.user.username:
            if vote['candidate'] == candidate.position:
                messages.warning(request, f'Ya ha votado por {candidate.position}.')
                return redirect('main')
    # Guardar información del voto en un archivo JSON
    vote_data = {
        'user': request.user.username,
        'candidate': candidate.position if candidate else None,
        'timestamp': timezone.now().isoformat(),
    }
    
    votes.append(vote_data)
    with open(votes_file, 'w', encoding='utf-8') as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)
    form.save(request.user)
    messages.success(request, 'Voto registrado exitosamente.')
    return redirect('main')

@login_required(login_url='logIn')
def results(request):
    if not request.user.is_superuser:
        logout(request)
        messages.error(request, 'No tienes permiso para ver los resultados.')
        return redirect('main')
    ombudsmans = Candidates.objects.filter(position='Personería')
    comptrollers = Candidates.objects.filter(position='Contraloría') 
    
    votes_ombudsman = sum(candidate.votes for candidate in ombudsmans)
    votes_comptroller = sum(candidate.votes for candidate in comptrollers)
    
    if votes_ombudsman > 0:
        for candidate in ombudsmans:
            candidate.percentage = (candidate.votes / votes_ombudsman) * 100 if votes_ombudsman > 0 else 0
            candidate.save()
    if votes_comptroller > 0:
        for candidate in comptrollers:
            candidate.percentage = (candidate.votes / votes_comptroller) * 100 if votes_comptroller > 0 else 0
            candidate.save()
        
    return render(request,'Users/results.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })