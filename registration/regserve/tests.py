from django.test import TestCase, Client

from .serializers import *
from .models import *
import io
from rest_framework.parsers import JSONParser
import logging

class DataTest(TestCase):
    #sets up logging
    def log_setup(logger_name, log_file, mode='w'):
        new_log = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        file_handler = logging.FileHandler(log_file, mode=mode)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        new_log.setLevel(logging.DEBUG)
        new_log.addHandler(file_handler)
        new_log.addHandler(stream_handler)
        return new_log
    #creates a test database for the tests to utilize
    def setUp(self):
        self.test_client = Client()
        Student.objects.create(
            firstname = "First",
            lastname = "Student",
            idnumber = 100,
            email = "first@student.edu",
            schoolyear = 'FR',
            major = 'CS',
            gpa = 4.0
        )
        Student.objects.create(
            firstname = "Second",
            lastname = "Student",
            idnumber = 101,
            email = "first@student.edu",
            schoolyear = 'SR',
            major = 'ENG',
            gpa = 2.0
        )
    #tests that database was created properly and is accessible, tests serializer for functionality
    def test_student_api(self):
        student_api_log = DataTest.log_setup("student_api", "../logs/student_api.log", 'w')
        student_response = self.test_client.get('/regserve/data/students/')
        student_api_log.info(f'STUDENT API TEST: inside test, response is {student_response} and the status code is {student_response.status_code}\n')
        self.assertEqual(student_response.status_code, 200)
        student_api_log.info(f'STUDENT API TEST: inside test, response content is {student_response.content}\n')
        student_stream = io.BytesIO(student_response.content)
        student_api_log.info(f'STUDENT API TEST: inside test, student stream is {student_stream}\n')
        student_api_data = JSONParser().parse(stream=student_stream)
        student_api_log.info(f'STUDENT API TEST: inside test, student api data is {student_api_data}\n')
        first_student_data = student_api_data[0]
        student_api_log.info(f'STUDENT API TEST: inside test, first student data is {first_student_data} id is {first_student_data["id"]}\n')
        first_student_db = Student.objects.get(id=first_student_data['id'])
        student_api_log.info(f'STUDENT API TEST: inside test, first student db is {first_student_db}\n')
        first_student_serializer = StudentSerializer(first_student_db, data=first_student_data)
        student_api_log.info(f'STUDENT API TEST: inside test, first student serializer is {first_student_serializer}\n')
        student_api_log.info(f'STUDENT API TEST: inside test, first student serializer data valid? {first_student_serializer.is_valid()}\n')
        first_student_api = first_student_serializer.save()
        student_api_log.info(f'STUDENT API TEST: inside test, first student API is {first_student_api}\n')
        self.assertEqual(first_student_api, first_student_db)

    #tests that student objects in the test database exist and are defined properly
    def test_student(self):
        student_list_log = DataTest.log_setup("student_list", "../logs/student_list.log", 'w')
        student_list = Student.objects.all()
        for student in student_list:
            student_list_log.info(f'Inside test_student, current student is {student}\n')
        student = student_list[0]
        self.assertEqual(student.id, 1)
        self.assertEqual(student.full_name, 'First Student')
        self.assertEqual(student.idnumber, 100)
        self.assertEqual(student.major, 'CS')
        self.assertEqual(student.gpa, 4.0)
    #tests delete functionality by deleting entire test database one object at a time and checks that database has changed
    def test_student_delete(self):
        student_delete_log = DataTest.log_setup("student_delete", "../logs/student_delete.log", 'w')
        original_student_list = Student.objects.all()
        student_delete_log.info(f'STUDENT DELETE TEST: inside test, original student list is {original_student_list}\n')
        for student in original_student_list:
            self.test_client.post(f'/regserve/deletestudent/{student.id}')
        new_student_list = Student.objects.all()
        student_delete_log.info(f'STUDENT DELETE TEST: inside test, new student list is {new_student_list}\n')
        self.assertNotEqual(original_student_list, new_student_list)
    #tests editing functionality by changing all test database entries to a specific student, checks that database changed and asserts all contents are correct
    def test_student_edit(self):
        student_edit_log = DataTest.log_setup("student edit", "../logs/student_edit.log", 'w')
        original_student_list = Student.objects.all()
        student_edit_log.info(f'STUDENT EDIT TEST: inside test, original student list is {original_student_list}\n')
        for student in original_student_list:
            self.test_client.post(f'/regserve/editstudent/{student.id}', {'firstname': 'John', 'lastname': 'Smith', 'idnumber': '200', 'schoolyear': 'FR', 'major': 'CS', 'gpa': '4.0'})
        new_student_list = Student.objects.all()
        student_edit_log.info(f'STUDENT EDIT TEST: inside test, new student list is {new_student_list}\n')
        self.assertNotEqual(original_student_list, new_student_list)
        for student in new_student_list:
            self.assertEqual(student.firstname, 'John')
            self.assertEqual(student.lastname, 'Smith')
            self.assertEqual(student.idnumber, 200)
            self.assertEqual(student.schoolyear, 'FR')
            self.assertEqual(student.major, 'CS')
            self.assertEqual(student.gpa, 4.0)
#intitial test for project setup
class SimpleTest(TestCase):
    def setUp(self):
        self.test_client = Client()
    #tests for a HTTP response from '/regserve'
    def test_response(self):
        simple_log = DataTest.log_setup("simple", "../logs/simple.log", 'w')
        response = self.test_client.get('/regserve')
        simple_log.info(f'Inside HW test, response is {response}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello from Django backend")
        
