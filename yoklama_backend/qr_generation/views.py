from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import generate_qr_token
from yoklama_data.models import AttendanceList, AttendanceRecord
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from student_data.models import Student
from math import *
from django.utils import timezone

class QRTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, attendance_list_id):
        try:
            attendance_list = AttendanceList.objects.get(id = attendance_list_id)
        except AttendanceList.DoesNotExist:
            return Response({"detail":"List not found"}, status=status.HTTP_404_NOT_FOUND)
        if attendance_list.hour.classroom is not None:
            classroom = attendance_list.hour.classroom
            if classroom.class_location is not None:
                class_location = classroom.class_location
            else: class_location = {"x": 0, "y": 0}
        else: class_location = {"x": 0, "y": 0}
        token = generate_qr_token(attendance_list_id, class_location)
        return Response({"qr_token": token})
    
class ValidateAttendanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student_id = request.data.get('student_id')
        student_location = request.data.get('student_location')
        class_location = request.data.get('classroom_location')
        attendance_list_id = request.data.get('attendance_list_id')
        exp = request.data.get('exp')
        token = request.headers.get('Authorization')

        if not token:
            return Response({"detail":"Token missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = JWTAuthentication().authenticate(request)
            if student_id != user[0].student_profile.id:
                return Response({"detail":"Invalid Student"}, status=status.HTTP_403_FORBIDDEN)
            
            if class_location is not None and not {"x": 0, "y": 0}:
                if not self.is_valid_location(student_location, class_location):
                    return Response({"detail":"Invalid location"}, status=status.HTTP_400_BAD_REQUEST)
            
            noww = int(timezone.now().timestamp())
            if noww > int(exp):
               return Response({"detail":"Expired"}, status=status.HTTP_400_BAD_REQUEST)

            self.record_attendance(student_id, attendance_list_id)
            return Response({"detail":"Attendance approved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
     
    def is_valid_location(self, student_location, class_location):
        
        # Convert latitude and longitude from degrees to radians
        class_lat = radians(float(class_location.get("x")))  # class latitude
        class_lon = radians(float(class_location.get("y")))  # class longitude
        student_lat = radians(float(student_location.get("x")))  # student latitude
        student_lon = radians(float(student_location.get("y")))  # student longitude

        # Haversine formula
        dlat = student_lat - class_lat
        dlon = student_lon - class_lon
        a = sin(dlat / 2) ** 2 + cos(class_lat) * cos(student_lat) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Earth's radius in meters (mean radius)
        radius = 6371000  # meters

        # Calculate the distance
        distance_in_meter = radius * c
        if distance_in_meter > 100.0:
            return False
        else: return True
    
    def record_attendance(self, student_id, attendance_list_id):
        student = Student.objects.get(id = student_id)
        attendance_list = AttendanceList.objects.get(id = attendance_list_id)
        attendance_record = AttendanceRecord.objects.get(student=student, attendance_list= attendance_list)
        attendance_record.is_attended = True
        attendance_record.save()


