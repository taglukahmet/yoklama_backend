from rest_framework import serializers
from .models import *
from lecturer_data.serializers import DepartmentSerializer
from lecturer_data.models import Department

class StudentSerializer(serializers.ModelSerializer):
    department_id = serializers.UUIDField(required=False)
    department = DepartmentSerializer(read_only=True,required=False)
    password = serializers.CharField(write_only= True,required=False)
    email = serializers.EmailField(write_only=True,required=False)
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'year', 'password' ,'email', 'student_number', 'department_id', 'department')
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
    




