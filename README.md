## A. Question:
The attached python file should be inserted into a new Django project, so that unit tests can be run against it. It should follow the principles of unit testing in that it only tests the many results depending on the inputs and mocked conditions, and minimizes exposure to external logic, but has checks to ensure that calls to external logic are made. It is expected to make heavy use of mocking.

Please use Django / Python for your solution. The logic and thought process demonstrated are the most important considerations rather than truly functional code, however code presentation is important as well as the technical aspect. If you cannot settle on a single perfect solution, you may also discuss alternative solutions to demonstrate your understanding of potential trade-offs as you encounter them. Of course if you consider a solution is too time consuming you are also welcome to clarify or elaborate on potential improvements or multiple solution approaches conceptually to demonstrate understanding and planned solution.
        def do_lots_of_things(a, b, c):
        """
        Tests a bunch of things
        :param a: int
        :param b: str
        :param c: datetime
        :return: int
        """
        validate_is_int(a)  # Raises django.core.exceptions.ValidationError('a is invalid')
        validate_is_string(b)  # Raises django.core.exceptions.ValidationError('b is invalid')
        validate_is_datetime(c)  # Raises django.core.exceptions.ValidationError('c is invalid')

        if (a == 2 or b != 'foo') or django.conf.settings.ALWAYS_CHECK_C:
          validate_is_next_year(c)  # Raises django.core.exceptions.ValidationError('c is not next year')

        if b == 'bar':
         return a * 3

         return a * django.conf.settings.MULTIPLY_A



## B.Solutions:

Firstly, to test a bunch of things which mentioned in the question we need to create a project contains of above parameters. I decided to choose the data of student information with three fields: Name of student (string format) , Age of student (int format) , and Birthdate of student (date time format).
### Step 1: Create project test_exam
django-admin startproject test_exam
### Step2: Create students app
python manage.py startapp students
### 1.	 model.py

    from django.db import models 

    class Student(models.Model):  
     name        = models.CharField(max_length=25, unique=True) 
     age         = models.IntegerField(null=False) 
     birthdate   = models.DateTimeField(null=False) 

     class Meta:                                     
        db_table = 'student'                         

     def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'birthdate': self.birthdate,
        }

### 2.	App

    from django.apps import AppConfig

    class StudentsConfig(AppConfig):
     default_auto_field = 'django.db.models.BigAutoField'
     name = 'students'

### 3.	Setting 

     INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'students'
     ] 
     ALWAYS_CHECK_C=True
     MULTIPLY_A=3


### 4. Service.py	:the requirement of “do_lots_of_things” will be carried out in Services: ProductionClass.Method 

     from django.core.exceptions import ValidationError
     import datetime
     from django.conf import settings
     MULTIPLY_A=settings.MULTIPLY_A
     ALWAYS_CHECK_C=settings.ALWAYS_CHECK_C
     class ProductionClass:
        @classmethod
        def method(cls, a, b, c):
            if not isinstance(a, int):
                raise ValidationError("This field accepts interger only")
            if not isinstance(b, str):
                raise ValidationError("This field accepts string only")
            if not isinstance(c, datetime):
                raise ValidationError("This field accepts datetime only")
            if(a==2 or b!='foo') or ALWAYS_CHECK_C==True:
             if c.year!=datetime.now.year+1:
                raise ValidationError("This field accepts datetime of next year only")
            if b=='bar':
                return a*3
            return a*MULTIPLY_A

### 5.	Test.py
### 5A) Service Test

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

### 5B) API TEST, Mock, Patch, Magic Mock

     with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
       thing = ProductionClass()
       thing.method(1, "a", datetime.now)

      mock_method.assert_called_once_with(1, "a", datetime.now)
     @patch('students.services.ProductionClass.method', return_value=3)
      def test_list_student(self, ProductionClass):
         response = client.get('/students/')
         result = {'data': []}
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.json(), result)


### 6.	View.py

     from django.shortcuts import render
     from django.http import JsonResponse
     from .models import Student
     from .services import ProductionClass
     def list_student(request):
      students = Student.objects.all()
      data = []
      for student in students:
        if ProductionClass.method(student.age,student.name,student.birthdate):
            data.append(student.to_json())
       return JsonResponse({'data': data})

### 7. URL

     from django.contrib import admin
     from django.urls import path
     from students import views as students_views
     urlpatterns = [
     path('admin/', admin.site.urls),
     path('students/', students_views.list_student, name='list_student')
     ]
