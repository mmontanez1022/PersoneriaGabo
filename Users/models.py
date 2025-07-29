from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Candidates(models.Model):
    POSITIONS = (
        ('Personería', 'Personería'),
        ('Contraloría', 'Contraloría'),
    )
    
    GRADES = (
        ('11-1', '11-1'),
        ('11-2', '11-2'),
        ('11-3', '11-3'),
        ('11-4', '11-4'),
        ('11-5', '11-5'),

    )
    
    GENDER = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification_number = models.IntegerField(unique=True)
    grade = models.CharField(
        max_length=10,
        choices=GRADES,
        default='11-1')
    age = models.IntegerField()
    position = models.CharField(
        max_length=20,
        choices=POSITIONS,
        default='Personería'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER, 
        default='Masculino'                     
    )
    description = models.TextField()
    photo = models.ImageField(upload_to='candidates_photos/', blank=True, null=True)
    votes = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
