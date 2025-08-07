from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#token lecturer_id inclusion
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'lecturer_profile'):
            token['lecturer_id'] = str(user.lecturer_profile.id)
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        if hasattr(self.user, 'lecturer_profile'):
            data['lecturer_id'] = str(self.user.lecturer_profile.id)
        return data

#for fetching the uni names for sign ups
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id','name')

#for fetching the faculty names for sign ups
class FacultySerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    class Meta:
        model = Faculty
        fields = ('id','name', 'university')

#for fetching the dept names for sign ups
class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    class Meta:
        model = Department
        fields = ('id', 'name', 'faculty')

#for posting info to the lecturer on sign ups
class LecturerSignUpSerializer(serializers.ModelSerializer):
    department_id = serializers.UUIDField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Lecturer
        fields = ('id', 'title', 'first_name', 'last_name', 'email', 'department_id', 'password', 'created_at')

    def create(self, validated_data):
        department_id = validated_data.pop('department_id')
        password = validated_data.pop('password')
        department = Department.objects.get(id=department_id)
        email = validated_data.pop('email')
        if User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError({"email":"A user with this email already exists"})
        user = User.objects.create_user(email=email, username=email, password=password)
        lecturer = Lecturer.objects.create(user=user, department=department, **validated_data)
        return lecturer

#for viewing and updating the lecturer in the profile page
class LecturerProfileSerializer(serializers.ModelSerializer):
    department_id = serializers.UUIDField(write_only = True, required=False)
    department_name = serializers.CharField(source='department.name',read_only = True)
    email = serializers.EmailField(source='user.email', read_only=True)
    email_update = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model= Lecturer
        fields = ('id', 'title', 'first_name', 'last_name', 'email', 'email_update', 'department_id', 'department_name', 'phone', 'profile_photo', 'created_at')
        read_only_fields = ('id', 'created_at')
    def update(self, instance, validated_data):
        department_id = validated_data.pop('department_id', None)
        if department_id:
            instance.department = Department.objects.get(id=department_id)
        if 'email_update' in validated_data:
            email = validated_data.pop('email_update')
            instance.user.email = email
            instance.user.username = email
            instance.user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
#for fetching lectures of a lecturer
################################################
class LectureforLecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'name', 'code', 'explicit_name')
class SectionforLecturerSerializer(serializers.ModelSerializer):
    lecture = LectureforLecturerSerializer(read_only=True)
    class Meta:
        model = Section
        fields = ('id', 'section_number', 'lecture')
class LecturerLecturesSerializer(serializers.ModelSerializer):
    sections = SectionforLecturerSerializer(many=True, read_only=True)
    class Meta:
        model = Lecturer
        fields = ('id', 'sections')
################################################

#for fetching the building for dropdown selects
class BuildingSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name',read_only=True)
    department_id = serializers.UUIDField(required=False)
    faculty_id = serializers.UUIDField(required=False)
    university_id = serializers.UUIDField(required=False)
    class Meta: 
        model = Building
        fields = ('id', 'department_name', 'name', 'department_id', 'faculty_id', 'university_id')

#for fetching the classroom for dropdown selects
class ClassroomSerializer(serializers.ModelSerializer):
    class_location = serializers.JSONField(required=False, read_only=True)
    building_id = serializers.UUIDField(required=False)
    class Meta:
        model = Classroom
        fields = ('id', 'name', 'building_id', 'class_location')

#for fetching the relevant Lecture details
class LectureSerializer(serializers.ModelSerializer):
    department_id = serializers.UUIDField(required=False)
    class Meta:
        model = Lecture
        fields = ('id', 'name', 'code', 'explicit_name', 'department_id' )
    
#for fetching, posting, putting sections
class SectionSerializer(serializers.ModelSerializer):
    lecture_id = serializers.UUIDField(required=False)
    lecture_name = serializers.CharField(source='lecture.name', read_only=True)
    lecture_code = serializers.CharField(source='lecture.code', read_only=True)
    lecturer_id = serializers.UUIDField(required=False)
    lecturer_title = serializers.CharField(source='lecturer.title', read_only=True)
    lecturer_first_name = serializers.CharField(source='lecturer.first_name', read_only=True)
    lecturer_last_name = serializers.CharField(source='lecturer.last_name', read_only=True)
    class Meta:
        model = Section
        fields = ('id', 'lecture_name', 'lecture_code', 'section_number', 'lecture_id', 'lecturer_title', 'lecturer_first_name', 'lecturer_last_name', 'lecturer_id')
        read_only_fields=('id',)
    def create(self, validated_data):
        lecture_id = validated_data.pop('lecture_id', None)
        lecture = Lecture.objects.get(id = lecture_id)
        lecturer_id = validated_data.pop('lecturer_id', None)
        lecturer = Lecturer.objects.get(id = lecturer_id)
        section = Section.objects.create(lecture = lecture, lecturer = lecturer, **validated_data)
        return section
    def update(self, instance, validated_data):
        lecturer_id = validated_data.pop('lecturer_id', None)
        if lecturer_id:
            instance.lecturer = Lecturer.objects.get(id=lecturer_id)
        else: instance.lecturer = None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def validate(self, data):
        lecture_id = data.get('lecture_id') or getattr(self.instance, 'lecture', None)
        section_number = data.get('section_number') or getattr(self.instance, 'section_number', None)
        if lecture_id and section_number:
            qs = Section.objects.filter(lecture=lecture_id, section_number=section_number)
            if self.instance:
                qs = qs.exclude(id = self.instance.id)
            if qs.exists():
                raise serializers.ValidationError(
                    {"section_number": "This section is already taken"}
                )
        return data

#for fetching, posting and putting hours
class HoursSerializer(serializers.ModelSerializer):
    section_id = serializers.UUIDField(required=False)
    section_number = serializers.CharField(source='section.section_number', read_only=True)
    lecture_name = serializers.CharField(source='section.lecture.name', read_only=True)
    lecture_code = serializers.CharField(source='section.lecture.code', read_only=True)
    classroom_id = serializers.UUIDField(required=False)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    building_name = serializers.CharField(source='classroom.building.name', read_only=True)
    order = serializers.CharField(required=False)
    day = serializers.CharField(required=False)
    time_start = serializers.TimeField(required=False)
    time_end = serializers.TimeField(required=False)
    class Meta:
        model = Hours
        fields = ('id', 'lecture_name', 'lecture_code', 'section_number', 'order', 'day', 'time_start', 'time_end', 'building_name', 'classroom_name', 'section_id', 'classroom_id')
        read_only_fields=('id',)
    def create(self, validated_data):
        section_id = validated_data.pop('section_id', None)
        section = Section.objects.get(id = section_id)
        classroom_id = validated_data.pop('classroom_id', None)
        classroom = Classroom.objects.get(id = classroom_id)
        hour = Hours.objects.create(section = section, classroom = classroom, **validated_data)
        return hour
    def update(self, instance, validated_data):
        classroom_id = validated_data.pop('classroom_id', None)
        if 'section' in validated_data:
            raise serializers.ValidationError({"section": "You can't change the section"})
        if classroom_id:
            instance.classroom = Classroom.objects.get(id=classroom_id)
        else: instance.classroom = None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def validate(self, data):
        section_id = data.get('section_id') or getattr(self.instance, 'section', None)
        order = data.get('order') or getattr(self.instance, 'order', None)
        if section_id and order:
            qs = Hours.objects.filter(section = section_id, order = order)
            if self.instance:
                qs = qs.exclude(id = self.instance.id)
            if qs.exists():
                raise serializers.ValidationError(
                    {"order": "This order already exists"}
                )
        return data

