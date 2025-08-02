from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login, logout

class UniversityListView(APIView):
    def get(self,request):
        universities = University.objects.all()
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FacultyListView(APIView):
    def get(self, request, university_id):
        faculties = Faculty.objects.filter(university_id=university_id)
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DepartmentListView(APIView):
    def get(self, request, faculty_id):
        departments = Department.objects.filter(faculty_id=faculty_id)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LecturerSignUpView(APIView):
    def post(self, request):
        serializer = LecturerSignUpSerializer(data=request.data)
        if serializer.is_valid():
            lecturer = serializer.save()
            return Response(LecturerSignUpSerializer(lecturer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LecturerProfileView(APIView):
    def get(self, request, lecturer_id):
        try:
            lecturer = Lecturer.objects.get(id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({"detail": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LecturerProfileSerializer(lecturer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, lecturer_id):
        try:
            lecturer = Lecturer.objects.get(id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({"detail": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LecturerProfileSerializer(lecturer, data=request.data)
        if serializer.is_valid():
            updated_lecturer = serializer.save()
            return Response(LecturerProfileSerializer(updated_lecturer).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BuildingView(APIView):
    def get(self, request, university_id):
        try:
            university = University.objects.get(id=university_id)
            buildings = Building.objects.filter(university = university)
        except University.DoesNotExist:
            return Response({"detail": "University not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ClassroomView(APIView):
    def get(self,request,building_id):
        classrooms = Classroom.objects.filter(building=building_id)
        if not classrooms.exists():
            return Response({"detail":"No classrooms found for this building."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LectureView(APIView):
    def get(self,request,department_id):
        lectures = Lecture.objects.filter(department = department_id)
        if not lectures.exists():
            return Response({"detail": "No courses found for this department."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SectionofLectureView(APIView):
    def get(self,request,lecture_id):
        sections = Section.objects.filter(lecture = lecture_id)
        if not sections.exists():
            return Response({"detail": "No sections found for this course."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, lecture_id):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save()
            return Response(SectionSerializer(section).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SectiononlyView(APIView):
    def get(self,request,section_id):
        try:
            section = Section.objects.get(id = section_id)
        except Section.DoesNotExist:
            return Response({"detail": "Section not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SectionSerializer(section)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, section_id):
        try:
            section = Section.objects.get(id = section_id)
        except Section.DoesNotExist:
            return Response({"detail": "Section not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SectionSerializer(section, data=request.data)
        if serializer.is_valid():
            updated_section = serializer.save()
            return Response(SectionSerializer(updated_section).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HoursofSectionView(APIView):
    def get(self,request,section_id):
        hours = Hours.objects.filter(section = section_id)
        if not hours.exists():
            return Response({"detail": "No hours found for this section."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HoursSerializer(hours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = HoursSerializer(data=request.data)
        if serializer.is_valid():
            hour = serializer.save()
            return Response(HoursSerializer(hour).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HouronlyView(APIView):
    def get(self,request,hour_id):
        try:
            hour = Hours.objects.get(id = hour_id)
        except Hours.DoesNotExist:
            return Response({"detail": "Hour not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HoursSerializer(hour)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, hour_id):
        try:
            hour = Hours.objects.get(id = hour_id)
        except Hours.DoesNotExist:
            return Response({"detail": "Hour not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HoursSerializer(hour, data=request.data)
        if serializer.is_valid():
            updated_hour = serializer.save()
            return Response(HoursSerializer(updated_hour).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)