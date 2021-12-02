from django.urls import path

from . import views

application = 'regserve'

urlpatterns = [
    path('data/students/', views.StudentListCreate.as_view()),
    path('', views.index, name='index'),
    ]