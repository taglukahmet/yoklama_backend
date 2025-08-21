from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from yoklama_backend.settings import API_CBU_DOMAIN, CBU_DOMAIN
import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken 
import hashlib

#token lecturer_id inclusion
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#cbu login view
class CBUAPILoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            domain = username.split('@')[1]
            if domain.lower() != CBU_DOMAIN:
                return Response({'error': 'Invalid credentials or user domain.'}, status=status.HTTP_401_UNAUTHORIZED)
        except IndexError:
            return Response({'error': 'Invalid username format.'}, status=status.HTTP_400_BAD_REQUEST)

        payload = {'username': username, 'password': password}

        response = requests.request("POST", API_CBU_DOMAIN, data=payload)
        responsed= response.json().get('user_data', {})

        hashed0 = responsed.get('description')[0]
        hashed1 = responsed.get('cn')[0]
        hashed = hashed0 + hashed1
        hashed_code = hashlib.sha256(hashed.encode('utf-8')).hexdigest()
        processed_profile = {
            'lecturer_id': hashed_code,
            'email': responsed.get('mail')[0],
            'first_name': responsed.get('givenname')[0],
            'last_name': responsed.get('sn')[0].capitalize(),
            'TC': hashed0,
            'department': responsed.get('department')[0]
        }

        refresh = RefreshToken()
        refresh['email'] = processed_profile['email']

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'profile': processed_profile
        }, status=status.HTTP_200_OK)

#returns all universities
class UniversityListView(APIView):
    def get(self,request):
        universities = University.objects.all()
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns faculties of a given university
class FacultyListView(APIView):
    def get(self, request, university_id):
        faculties = Faculty.objects.filter(university_id=university_id)
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns departments of a given faculty
class DepartmentListView(APIView):
    def get(self, request, faculty_id):
        departments = Department.objects.filter(faculty_id=faculty_id)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#for lecturers to signup
class LecturerSignUpView(APIView):
    def post(self, request):
        serializer = LecturerSerializer(data=request.data)
        if serializer.is_valid():
            lecturer = serializer.save()
            return Response(LecturerSerializer(lecturer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#returns all info except password 
class LecturerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, lecturer_id):
        try:
            lecturer = Lecturer.objects.get(id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({"detail": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LecturerSerializer(lecturer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, lecturer_id):
        try:
            lecturer = Lecturer.objects.get(id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({"detail": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LecturerSerializer(lecturer, data=request.data)
        if serializer.is_valid():
            updated_lecturer = serializer.save()
            return Response(LecturerSerializer(updated_lecturer).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#returns dept, fac, and uni ids if any alongside building info of a uni
class BuildingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, university_id):
        try:
            university = University.objects.get(id=university_id)
            buildings = Building.objects.filter(university = university)
        except University.DoesNotExist:
            return Response({"detail": "University not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns classrooms of a building, and classroom locations
class ClassroomView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,building_id):
        classrooms = Classroom.objects.filter(building=building_id)
        if not classrooms.exists():
            return Response({"detail":"No classrooms found for this building."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns the lectures of a given department
class LectureView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,department_id):
        lectures = Lecture.objects.filter(department = department_id)
        if not lectures.exists():
            return Response({"detail": "No courses found for this department."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns the lectures of a lecturer
class LecturesofLecturerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,lecturer_id):
        try:
            lecturer = Lecturer.objects.get(id = lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({"detail":"Lecturer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LecturerLecturesSerializer(lecturer)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns the lectures of a lecturer
class CBULecturesofLecturerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,lecturer_tc):
        sections = Section.objects.filter(lecturer_tc = lecturer_tc)
        if not sections.exists():
            return Response({"detail": "There are no sections for the Teacher or Teacher not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CBUSectionforLecturerSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#returns section info to  add one into the lecture   
class SectionofLectureView(APIView):
    permission_classes = [IsAuthenticated]
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

#returns section spesific info to edit    
class SectiononlyView(APIView):
    permission_classes = [IsAuthenticated]
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

#returns hours of sections to add
class HoursofSectionView(APIView):
    permission_classes = [IsAuthenticated]
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

#returns hour spesific info to edit
class HouronlyView(APIView):
    permission_classes = [IsAuthenticated]
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