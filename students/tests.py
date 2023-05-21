from django.test import TestCase
import json
from .models import Student
from .services import ProductionClass
from django.test       import TestCase
from django.test       import Client
from unittest.mock     import patch, MagicMock
from django.core.exceptions import ValidationError
#from contextlib import contextmanager
import datetime

client = Client()

# Create your tests here.
class StudentTest_API(TestCase):

    def setUp(self):
        Student.objects.create(
            name = 'Brendan Eich',
            age = 10,
            birthdate=datetime.date(2010, 1, 1)
        )
        Student.objects.create(
            name = 'Minh',
            age = 30,
            birthdate=datetime.date(2007, 1, 1)
        )

    def tearDown(self):
        Student.objects.all().delete()

    @patch('students.services.ProductionClass.method', return_value=3)
    def test_students(self, method):
        response = client.get('/students/')
        result = {'data': []}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
    


class StudentTests_Service(TestCase):
    def test_not_integer(self):
        is_integer = ProductionClass.method("A","B",datetime.date(2022,1,2))
        self.assertEqual(is_integer, "This field accepts interger only")

    def test_not_string(self):
        is_string = ProductionClass.method(2,5,datetime.date(2022,1,2))
        self.assertEqual(is_string, ("This field accepts string only"))

    def test_not_datetime(self):
        is_datetime = ProductionClass.method(2,"b",7)
        self.assertEqual(is_datetime, ("This field accepts datetime only")) 
    
    def test_string_bar(self):
        is_3a = ProductionClass.method(3,"bar",datetime.date(2022,1,2))
        self.assertEqual(is_3a, 9)

                        

    
        
with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
     thing = ProductionClass()
     thing.method(1, "a", datetime.now)

     mock_method.assert_called_once_with(1, "a", datetime.now)
@patch('students.services.ProductionClass.method', return_value=3)
def test_list_students(self, ProductionClass):
        response = client.get('/students/')
        result = {'data': []}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)