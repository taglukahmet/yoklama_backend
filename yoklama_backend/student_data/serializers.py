from rest_framework import serializers
from .models import *
from yoklama_data.models import StudentList
from lecturer_data.models import Department
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#for student login and auth tokens, also for returning student_id
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'student_profile'):
            token['student_id'] = str(user.student_profile.id)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if hasattr(self.user, 'student_profile'):
            data['student_id'] = str(self.user.student_profile.id)
        return data

#student info returns, password is safe
class StudentSerializer(serializers.ModelSerializer):
    department_id = serializers.UUIDField(required=False, write_only=True)
    department_name = serializers.CharField(source='department.name',read_only = True)
    password = serializers.CharField(write_only= True,required=False)
    email = serializers.EmailField(write_only=True,required=False)
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'year', 'department_name', 'department_id', 'student_number', 'password' ,'email')
    def create(self, validated_data):
        department_id = validated_data.pop('department_id')
        department = Department.objects.get(id = department_id)
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        if User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError({"email":"A user with this email already exists"})
        user = User.objects.create_user(email=email, username=email, password=password)
        student = Student.objects.create(user=user, department=department, **validated_data)
        return student
    def update(self, instance, validated_data):
        department_id = validated_data.pop('department_id', None)
        if department_id:
            instance.department = Department.objects.get(id = department_id)
        if 'email' in validated_data:
            email = validated_data.pop('email')
            instance.user.email = email
            instance.user.username = email
            instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
#for fetching lectures of a student
################################################
class StudentsListsSerializer(serializers.ModelSerializer):
    lecture_id = serializers.UUIDField(source='section.lecture.id', required=False, write_only=True)
    section_id = serializers.UUIDField(required=False, write_only=True)
    lecturer_id = serializers.UUIDField(source='section.lecturer.id', required=False, write_only=True)
    lecture_name = serializers.CharField(source='section.lecture.name', read_only=True)
    lecture_code = serializers.CharField(source='section.lecture.code', read_only=True)
    section_number = serializers.CharField(source='section.section_number', read_only=True)
    lecturer_title = serializers.CharField(source='section.lecturer.title', read_only=True)
    lecturer_first_name = serializers.CharField(source='section.lecturer.first_name', read_only=True)
    lecturer_last_name = serializers.CharField(source='section.lecturer.last_name', read_only=True)

    class Meta:
        model = StudentList 
        fields = ('id', 'lecture_name', 'lecture_code', 'section_number', 'lecturer_title', 'lecturer_first_name', 'lecturer_last_name', 'lecture_id', 'section_id', 'lecturer_id')

class StudentLecturesSerializer(serializers.ModelSerializer):
    enrolled_lists = StudentsListsSerializer(many=True, read_only=True) 

    class Meta:
        model = Student
        fields = ('id', 'enrolled_lists')
################################################



