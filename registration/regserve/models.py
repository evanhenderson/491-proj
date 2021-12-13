from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse, reverse_lazy
# Create your models here.
#Person class defines all fields for students to inherit, would have been shared by teachers if implemented
class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    idnumber = models.PositiveBigIntegerField()
    email = models.EmailField(blank=True)
    datecreated = models.DateTimeField(blank=True, auto_now_add=True)
    datemodified = models.DateTimeField(blank=True, auto_now=True)

    @property
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        abstract = True

    def __str__(self):
        return f'Name: {self.full_name}, Id Number: {self.idnumber}, email: {self.email}'
    
#inherits Person, defines all possible values for schoolyear and majors fields
class Student(Person):
    YEAR_IN_SCHOOL = [
        ('FR', 'Freshman'),
        ('SO', 'Sophmore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate')
    ]

    MAJORS = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('SC', 'Science'),
        ('BUS', 'Business'),
        ('LAW', 'Law'),
        ('NUR', 'Nursing'),
        ('MAT', 'Math')
    ]
    schoolyear = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL)
    major = models.CharField(max_length=3, choices=MAJORS)
    gpa = models.FloatField(max_length=4, blank=True)
    #defines how the object is converted to a str
    def __str__(self):
        return f'StudentId: {self.id}: {super(Student, self).__str__()}, year in school: {self.schoolyear}, major: {self.major}, GPA: {self.gpa}'
    #uses revers_lazy function to get an absolute url
    def get_absolute_url(self):
        return reverse_lazy('registration:students')
