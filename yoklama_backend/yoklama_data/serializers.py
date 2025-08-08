from .models import *
from rest_framework import serializers
from lecturer_data.models import Section, Hours
from lecturer_data.serializers import SectionSerializer, HoursSerializer
from student_data.models import Student
from student_data.serializers import StudentSerializer

class StudentListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    section_id = serializers.UUIDField(required=False)
    students = StudentSerializer(many=True, read_only=True)
    student_numbers = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    class Meta:
        model = StudentList
        fields = ('id', 'name', 'section_id', 'student_numbers', 'students')
        read_only_fields = ('id',)
    def create(self, validated_data):
        section_id = validated_data.pop('section_id', None)
        section = Section.objects.get(id=section_id)
        student_numbers = validated_data.pop('student_numbers', [])
        student_list = StudentList.objects.create(section = section, **validated_data)
        if student_numbers:
            university = section.lecture.department.faculty.university
            students = Student.objects.filter(department__faculty__university = university, student_number__in=student_numbers)
            student_list.students.set(students)
        return student_list
    def update(self, instance, validated_data):
        section_id = validated_data.pop('section_id', None)
        if section_id is not None:
            section = Section.objects.get(id=section_id)    
            instance.section = section
        student_numbers = validated_data.pop('student_numbers', None)
        if student_numbers is not None:
            university = section.lecture.department.faculty.university
            students = Student.objects.filter(department__faculty__university = university, student_number__in=student_numbers)
            instance.students.set(students)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class AttendanceRecordSerializer(serializers.ModelSerializer):
    attendance_list_id = serializers.UUIDField(required=False)
    student = StudentSerializer(read_only=True)
    student_id = serializers.UUIDField(required=False)
    class Meta:
        model = AttendanceRecord
        fields = ('id', 'is_attended', 'student_id', 'student', 'attendance_list_id', 'created_at')
        read_only_fields = ('id', 'created_at')
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class AttendanceListSerializer(serializers.ModelSerializer):
    attendance_records = AttendanceRecordSerializer(many=True, read_only=True)
    student_list_id = serializers.UUIDField(required = False)
    hour_id = serializers.UUIDField(required = False)
    class Meta:
        model = AttendanceList
        fields = ('id', 'is_active', 'is_taken_rollcall', 'hour_id', 'student_list_id', 'attendance_records', 'created_at')
        read_only_fields = ('id', 'created_at')
    def create(self, validated_data):
        hour_id = validated_data.pop('hour_id')
        hour = Hours.objects.get(id = hour_id)
        student_list_id = validated_data.pop('student_list_id', None)
        student_list = StudentList.objects.get(id = student_list_id)
        attendance_list = AttendanceList.objects.create(hour = hour, student_list= student_list, **validated_data)
        for student in student_list.students.all():
            AttendanceRecord.objects.create(student=student, attendance_list=attendance_list, is_attended = False) 
        return attendance_list
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


