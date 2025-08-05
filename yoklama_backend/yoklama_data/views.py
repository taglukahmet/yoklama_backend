from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.utils.dateparse import parse_date
from datetime import datetime

class StudentListView(APIView):
    def get(self, request,section_id):
        try:
            student_list = StudentList.objects.get(section = section_id)
        except StudentList.DoesNotExist:
            return Response({"detail":"List not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentListSerializer(student_list)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, section_id):
        serializer = StudentListSerializer(data = request.data)
        if serializer.is_valid():
            student_list = serializer.save()
            return Response(StudentListSerializer(student_list).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, section_id):
        try:
            student_list = StudentList.objects.get(section = section_id)
        except StudentList.DoesNotExist:
            return Response({"detail":"List not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentListSerializer(student_list, data=request.data)
        if serializer.is_valid():
            updated_student_list = serializer.save()
            return Response(StudentListSerializer(updated_student_list).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceListofHourView(APIView):
    def get(self, request, hour_id):
        date_str = request.query_params.get('date', None)
        filters = {'hour': hour_id}

        if date_str:
            try:
                date = parse_date(date_str)
                filters['created_at__date'] = date  # ← switched to created_at
            except Exception:
                return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendance_list = AttendanceList.objects.get(**filters)
        except AttendanceList.DoesNotExist:
            return Response({"detail": "List not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceListSerializer(attendance_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, hour_id):
        date_str = request.query_params.get('date', None)

        if date_str:
            try:
                date = parse_date(date_str)
                existing = AttendanceList.objects.filter(hour=hour_id, created_at__date=date)  # ← switched to created_at
                if existing.exists():
                    return Response({"detail": "Attendance list for this hour and date already exists."}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttendanceListSerializer(data=request.data)
        if serializer.is_valid():
            attendance_list = serializer.save()
            return Response(AttendanceListSerializer(attendance_list).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, hour_id):
        date_str = request.query_params.get('date', None)
        filters = {'hour': hour_id}

        if date_str:
            try:
                date = parse_date(date_str)
                filters['created_at__date'] = date  # ← switched to created_at
            except:
                return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendance_list = AttendanceList.objects.get(**filters)
        except AttendanceList.DoesNotExist:
            return Response({"detail": "List not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceListSerializer(attendance_list, data=request.data)
        if serializer.is_valid():
            updated_attendance_list = serializer.save()
            return Response(AttendanceListSerializer(updated_attendance_list).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceListofStudentListView(APIView):
    def get(self, request, student_list_id):
        attendance_lists = AttendanceList.objects.filter(student_list = student_list_id)
        if not attendance_lists.exists():
            return Response({"detail":"No attendance lists found for this student list"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceListSerializer(attendance_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, student_list_id):
        serializer = AttendanceListSerializer(data = request.data)
        if serializer.is_valid():
            attendance_list = serializer.save()
            return Response(AttendanceListSerializer(attendance_list).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AttendanceRecordofAttendanceListView(APIView):
    def get(self, request, attendance_list_id):
        attendance_records = AttendanceRecord.objects.filter(attendance_list = attendance_list_id)
        if not attendance_records.exists():
            return Response({"detail":"No attendance records found for this attendance list"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceRecordSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, attendance_list_id):
        serializer = AttendanceRecordSerializer(data = request.data)
        if serializer.is_valid():
            attendance_record = serializer.save()
            return Response(AttendanceRecordSerializer(attendance_record).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class AttendanceRecordOnlyView(APIView):
    def get(self, request,attendance_record_id):
        try:
            attendance_record = AttendanceRecord.objects.get(id = attendance_record_id)
        except AttendanceRecord.DoesNotExist:
            return Response({"detail":"Record not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceRecordSerializer(attendance_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, attendance_record_id):
        try:
            attendance_record = AttendanceRecord.objects.get(id = attendance_record_id)
        except AttendanceRecord.DoesNotExist:
            return Response({"detail":"List not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceRecordSerializer(attendance_record, data=request.data)
        if serializer.is_valid():
            updated_attendance_record = serializer.save()
            return Response(AttendanceRecordSerializer(updated_attendance_record).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





