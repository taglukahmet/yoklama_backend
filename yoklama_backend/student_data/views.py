from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudentofDepartmentView(APIView):
    def post(self, request, department_id):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, department_id):
        students = Student.objects.filter(department=department_id)
        if not students.exists():
            return Response({"detail": "No students found for this department."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StudentonlyView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id = student_id)
        except Student.DoesNotExist:
            return Response({"detail":"Student not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, student_id):
        try:
            student = Student.objects.get(id = student_id)
        except Student.DoesNotExist:
            return Response({"detail":"Student not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data = request.data)
        if serializer.is_valid():
            updated_student = serializer.save()
            return Response(StudentSerializer(updated_student).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





