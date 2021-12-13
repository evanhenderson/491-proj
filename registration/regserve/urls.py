from django.urls import path

from . import views

app_name = 'regserve'

urlpatterns = [
    path('/students/', views.StudentListForm.as_view(), name="students"),
    path('/createstudent/', views.StudentCreateForm.as_view(), name="create_students"),
    path('data/students/', views.StudentListCreate.as_view()),
    path('/deletestudent/<int:pk>', views.StudentDelete.as_view(), name="delete_student"),
    path('/editstudent/<int:pk>', views.StudentEdit.as_view(), name="edit_student"),
    path('', views.index, name='index'),
    ]