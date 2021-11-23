from django.urls import path

from . import views

application = 'regserve'

urlpatterns = [
    path('', views.index, name='index'),
    ]