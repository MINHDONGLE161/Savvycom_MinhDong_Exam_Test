from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
from .services import ProductionClass


def list_student(request):
    students = Student.objects.all()
    data = []
    for student in students:
        if ProductionClass(student.age,student.name,student.birthdate):
            data.append(student.to_json())
    return JsonResponse({'data': data})


