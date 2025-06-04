from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Candidates

class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {'' for _ in fields}
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email

class CandidateForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Usuario'
    )
    identification_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Número de Identificación'
    )
    grade = forms.ChoiceField(
        choices=[
            ('', 'Seleccione un grado')
        ] + [(f'11-{str(i)}',f'11-{str(i)}') for i in range(1, 6)],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Grado'
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Edad'
    )
    position = forms.ChoiceField(
        choices=[('', 'Seleccione el cargo'),('Personería', 'Personería'),('Contraloría', 'Contraloría')],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Posición'
    )
    gender = forms.ChoiceField(
        choices=[('', 'Seleccione el género'), ('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Género'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Descripción'
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Foto'
    )
    class Meta:
        model = Candidates
        fields = ['user', 'identification_number', 'grade', 'age', 'position', 'gender', 'description', 'photo']
        help_texts = {'' for _ in fields}
