from django.test import TestCase, Client

from registration.regserve.serializers import StudentSerializer
from .models import *
import io
from rest_framework.parsers import JSONParser
import logging

class DataTest(TestCase):
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
    def setUp(self):
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

    def test_student_api(self):
        student_api_log = DataTest.log_setup("student_api", "/491Proj/logs/student_api.log", 'w')
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


    def test_student(self):
        student_list_log = DataTest.log_setup("student_list", "/491Proj/logs/student_list.log", 'w')
        student_list = Student.objects.all()
        for student in student_list:
            student_list_log.info(f'Inside test_student, current student is {student}\n')
        student = student_list[0]
        self.assertEqual(student.id, 1)
        self.assertEqual(student.full_name, 'First Student')
        self.assertEqual(student.idnumber, 100)
        self.assertEqual(student.major, 'CS')
        self.assertEqual(student.gpa, 4.0)
class SimpleTest(TestCase):
    def setUp(self):
        self.test_client = Client()

    def test_response(self):
        simple_log = DataTest.log_setup("simple", "/491Proj/logs/simple.log", 'w')
        response = self.test_client.get('/regserve')
        simple_log.info(f'Inside HW test, response is {response}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello from Django backend")
        
