from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Student(models.Model):
    studentid = models.PositiveIntegerField(validators=(MinValueValidator(1)))
