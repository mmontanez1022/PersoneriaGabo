from django.db import models
from django.contrib.auth.models import User

class Candidates(models.Model):
    # Opciones de cargos a los que se pueden postular
    POSITIONS = (
        ('Personería', 'Personería'),
        ('Contraloría', 'Contraloría'),
    )
    
    # Opciones de grados disponibles
    GRADES = (
        ('11-1', '11-1'),
        ('11-2', '11-2'),
        ('11-3', '11-3'),
        ('11-4', '11-4'),
        ('11-5', '11-5'),
    )
    
    # Opciones de género
    GENDER = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    )
    
    # Relación uno a uno con el usuario del sistema
    # Cada candidato corresponde a un usuario registrado
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Documento de identidad único por cada candidato
    identification_number = models.IntegerField(unique=True)

    # Grado del candidato (obligatorio escoger de GRADES)
    grade = models.CharField(
        max_length=10,
        choices=GRADES,
        default='11-1'
    )

    # Edad del candidato
    age = models.IntegerField()

    # Cargo al que se postula (obligatorio escoger de POSITIONS)
    position = models.CharField(
        max_length=20,
        choices=POSITIONS,
        default='Personería'
    )

    # Género del candidato
    gender = models.CharField(
        max_length=10,
        choices=GENDER, 
        default='Masculino'                     
    )

    # Descripción breve del candidato (para campaña, propuestas, etc.)
    description = models.TextField()

    # Foto del candidato (con ruta por defecto en caso de no subir ninguna)
    photo = models.ImageField(
        upload_to='candidates_photos/', 
        blank=True, 
        null=True,
        default='candidates_photos/default.jpg'
    )

    # Contador de votos obtenidos
    votes = models.IntegerField(default=0)

    # Porcentaje de votos (se calcula en resultados)
    percentage = models.FloatField(default=0.0)
