from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework import serializers
from .serializers import *
from rest_framework import generics
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

# Create your views here.
def index(request):
    return HttpResponse("Hello from Django backend")

class StudentDelete(DeleteView):
    model = Student
    pk_url_kwarg = 'pk'
    template_name = 'regserve/student_delete_form.html'
    success_url = 'regserve/students'

class StudentEdit(UpdateView, ListView):
    model = Student
    pk_url_kwarg = 'pk'
    template_name = 'regserve/student_edit_form.html'
    success_url = 'regserve/students'
    fields = ['firstname', 'lastname', 'idnumber', 'schoolyear', 'major', 'gpa']

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentListForm(ListView):
    model = Student

class StudentCreateForm(CreateView, ListView):
    model = Student
    fields = ['firstname', 'lastname', 'idnumber', 'schoolyear', 'major', 'gpa']
