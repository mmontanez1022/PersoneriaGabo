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


# Importaciones necesarias
@login_required(login_url='logIn')   # Obliga a estar logueado para acceder a la vista
def signUp(request):
    # Solo el superusuario puede crear nuevos usuarios
    if not request.user.is_superuser:
        logout(request)  # Expulsa al usuario
        messages.error(request, 'No tienes permiso para crear usuarios.')
        return redirect('main')
    
    if request.method == 'GET':
        # Renderiza el formulario vacío en GET
        return render(request,'users/signUp.html',{
            'form': UserRegisterForm()
        })
    else:
        # Si viene un POST, valida y guarda el formulario
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request,'users/signUp.html',{
                'form': form
            })
        user = form.save()  # Crea el usuario
        return redirect('main')


def logIn(request):
    if request.method == 'GET':
        return render(request,'users/logIn.html')   
    else:
        # Busca el usuario por correo electrónico
        try:
            user = User.objects.get(email=request.POST['email'])
        except User.DoesNotExist:
            messages.error(request, 'La contraseña o el correo electrónico son incorrectos.')
            return render(request,'users/logIn.html')
        
        # Autenticación usando username (porque Django no usa email por defecto)
        user = authenticate(username=user.username, password=request.POST['password'])
        if user is None:
            messages.error(request, 'La contraseña o el correo electrónico son incorrectos.')
            return render(request,'users/logIn.html')
        
        # Si el usuario ya votó, lo bloquea
        if not user.is_active:
            messages.error(request, 'El usuario ya votó.')
            return render(request,'users/logIn.html')
        
        # Inicia sesión
        login(request, user)
        return redirect('main')


def logOut(request):
    # Cierra la sesión y redirige al login
    logout(request)
    return redirect('logIn')


@login_required(login_url='logIn')
def main(request):
    # Separa candidatos por cargo
    ombudsmans = Candidates.objects.filter(position='Personería')
    comptrollers = Candidates.objects.filter(position='Contraloría')
    
    if request.method == 'GET':
        # Muestra todos los candidatos en GET
        return render(request,'users/main.html',{
            'candidates': Candidates.objects.all(),
        })
    else:
        # Devuelve datos específicos en POST
        return render(request,'users/main.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })


@login_required(login_url='logIn')
def create_candidate(request):
    # Solo el superusuario puede crear candidatos
    if not request.user.is_superuser:
        logout(request)
        messages.error(request, 'No tienes permiso para crear candidatos.')
        return redirect('main')
    
    users = User.objects.filter(is_active=True)   # Usuarios activos
    candidates = Candidates.objects.all()         # Lista de candidatos
    
    if request.method == 'GET':
        return render(request,'users/create_candidate.html',{
            'form': CandidateForm(),
            'users': users,
            'candidates' : candidates
        })
    else:
        # Si POST, valida y guarda
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
    # Solo permite POST
    if request.method != 'POST':
        return redirect('main')
    
    # El admin no puede votar
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'No tienes permiso para votar.')
        return redirect('main')
    
    form = VoteForm(request.POST)
    
    # Busca al candidato
    try:
        candidate = Candidates.objects.get(id=request.POST.get('candidate'))
    except Candidates.DoesNotExist:
        candidate = None
    
    if not form.is_valid():
        messages.error(request, 'Hubo un error al votar.')
        return redirect('main')
    
    # Archivo JSON donde se guardan los votos
    votes_file = os.path.join(os.path.dirname(__file__), 'votes.json')
    try:
        with open(votes_file, 'r', encoding='utf-8') as f:
            votes = json.load(f)
            print(votes)
    except (FileNotFoundError, json.JSONDecodeError):
        votes = []
    
    # Verifica si el usuario ya votó para esa posición
    for vote in votes:
        if vote['user'] == request.user.username:
            if vote['candidate'] == candidate.position:
                messages.warning(request, f'Ya ha votado por {candidate.position}.')
                return redirect('main')
    
    # Registro del voto
    vote_data = {
        'user': request.user.username,
        'candidate': candidate.position if candidate else None,
        'timestamp': timezone.now().isoformat(),
    }
    
    # Agregar al archivo JSON
    votes.append(vote_data)
    with open(votes_file, 'w', encoding='utf-8') as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)
    
    # Guardar voto en la BD
    form.save(request.user)
    messages.success(request, 'Voto registrado exitosamente.')
    return redirect('main')


@login_required(login_url='logIn')
def results(request):
    # Solo admin puede ver resultados
    if not request.user.is_superuser:
        logout(request)
        messages.error(request, 'No tienes permiso para ver los resultados.')
        return redirect('main')
    
    # Candidatos por cargo
    ombudsmans = Candidates.objects.filter(position='Personería')
    comptrollers = Candidates.objects.filter(position='Contraloría') 
    
    # Conteo de votos
    votes_ombudsman = sum(candidate.votes for candidate in ombudsmans)
    votes_comptroller = sum(candidate.votes for candidate in comptrollers)
    
    # Calcula porcentaje para Personería
    if votes_ombudsman > 0:
        for candidate in ombudsmans:
            candidate.percentage = (candidate.votes / votes_ombudsman) * 100
            candidate.save()
    
    # Calcula porcentaje para Contraloría
    if votes_comptroller > 0:
        for candidate in comptrollers:
            candidate.percentage = (candidate.votes / votes_comptroller) * 100
            candidate.save()
        
    # Renderiza resultados
    return render(request,'Users/results.html',{
            'ombudsmans' : ombudsmans,
            'comptrollers' : comptrollers,
        })
