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
    # test case validate_is_int(a).
    def test_not_integer(self):
        is_integer = ProductionClass.method("A","B",datetime.date(2022,1,2))
        self.assertEqual(is_integer, "This field accepts interger only")

    # test case validate_is_string(b).
    def test_not_string(self):
        is_string = ProductionClass.method(2,5,datetime.date(2022,1,2))
        self.assertEqual(is_string, ("This field accepts string only"))
    
    # test case Validate_is_datetime(c)
    def test_not_datetime(self):
        is_datetime = ProductionClass.method(2,"b",7)
        self.assertEqual(is_datetime, ("This field accepts datetime only")) 

    # test case  validate_is_next_year(c) if a =2 or b !="foo"
    def test_nextyear(self):
        is_nextyear = ProductionClass.method(2,"a",datetime.date(2024,1,2))
        self.assertEqual(is_nextyear, ("This field accepts datetime of next year only"))

    
    # test case if b="bar", return a*3 
    def test_string_bar(self):
        is_3a = ProductionClass.method(3,"bar",datetime.date(2022,1,2))
        self.assertEqual(is_3a, 9)

    # test case return a * django.conf.settings.MULTIPLY_A (example MULTIPLY_A=5)
    def test_return(self):
        is_return = ProductionClass.method(7,"B",datetime.date(2022,1,2))
        self.assertEqual(is_return, 35)

                        

    
        
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