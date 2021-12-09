from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework import serializers
from .serializers import *
from rest_framework import generics
from django.views.generic import ListView, CreateView

# Create your views here.
def index(request):
    return HttpResponse("Hello from Django backend")

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentListForm(ListView):
    model = Student
