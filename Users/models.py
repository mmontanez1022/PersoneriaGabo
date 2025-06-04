from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Candidates(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification_number = models.IntegerField(unique=True)
    grade = models.CharField(max_length=10)
    age = models.IntegerField()
    position = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    description = models.TextField()
    photo = models.ImageField(upload_to='candidates_photos/', blank=True, null=True)
    votes = models.IntegerField(default=0)
