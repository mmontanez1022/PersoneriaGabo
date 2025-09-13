from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Candidates

# Formulario de registro de usuarios
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        #Elimina todos los textos de ayuda por defecto.
        help_texts = {field: "" for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega la clase Bootstrap "form-control" a cada campo
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    # Validación personalizada para el email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email


# Formulario de creación de candidatos
class CandidateForm(forms.ModelForm):
    # Relación con usuario existente
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Usuario'
    )
    # Documento de identidad
    identification_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Número de Identificación'
    )
    # Grado (con opciones dinámicas del 11-1 al 11-5)
    grade = forms.ChoiceField(
        choices=[('', 'Seleccione un grado')] + [(f'11-{i}', f'11-{i}') for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Grado'
    )
    # Edad
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Edad'
    )
    # Cargo (personero o contralor)
    position = forms.ChoiceField(
        choices=[('', 'Seleccione el cargo'), ('Personería', 'Personería'), ('Contraloría', 'Contraloría')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Posición'
    )
    # Género
    gender = forms.ChoiceField(
        choices=[('', 'Seleccione el género'), ('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Género'
    )
    # Descripción del candidato
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Descripción'
    )
    # Foto del candidato (opcional)
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Foto'
    )

    class Meta:
        model = Candidates
        fields = ['user', 'identification_number', 'grade', 'age', 'position', 'gender', 'description', 'photo']
        help_texts = {field: "" for field in fields}  


# Formulario de votación
class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(
        queryset=Candidates.objects.all()
    )
    
    def save(self, user, active=False):
        # Validación: el usuario debe existir y no debe haber votado antes
        if not user and isinstance(user, User):
            raise ValidationError('El usuario no existe o ya votó.')
        
        # Desactiva al usuario si se indica (para evitar votos duplicados)
        if active:  
            user.is_active = False
            user.save()
        
        # Suma el voto al candidato
        candidate = self.cleaned_data.get('candidate')
        if candidate:
            candidate.votes += 1
            candidate.save()
