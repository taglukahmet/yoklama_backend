from django.db import models
from django.utils import timezone
from django.db.models import JSONField, Q
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class University(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100, unique=True)
    academic_calendar_dates= models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name}"

class Faculty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')

    def __str__(self):
        return f"{self.name}"

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="", null=False, max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name}"

class Lecturer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(default="", null=False, max_length=30)
    first_name = models.CharField(default="", null=False, max_length=100)
    last_name = models.CharField(default="", null=False, max_length=100) 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='lecturers')
    email = models.EmailField(default="", null=False)
    phone = PhoneNumberField(null=True, blank=True, region='TR')
    profile_photo = models.ImageField(upload_to='lecturer_photos/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="", null=False, max_length=6)
    code = models.CharField(default="", null=False, max_length=6)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lectures')
    explicit_name = models.CharField(default="", null=True, blank=True, max_length=100)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['code', 'department'], name='unique_code_per_department')
        ]
    
    def __str__(self):
        return f"{self.name} {self.code}"
    
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section_number = models.CharField(default="", null=False, max_length=6)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='sections')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank = True, related_name='sections')
    
    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['lecture', 'section_number'], name='unique_section_per_lecture')
        ]

    def __str__(self):
        return f"{self.lecture.full_name} Section-{self.section_number}"

class Building(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100)
    department= models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='blocks')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True, related_name='blocks')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='blocks')

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['department', 'name'], condition=Q(department__isnull=False), name='unique_block_per_dept')
        ]
    
    def __str__(self):
        if self.department: return f"{self.department.name} {self.name}"
        elif self.faculty : return f"{self.faculty.name} {self.name}"
        else: return f"{self.name}"

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100)
    building= models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classes')
    class_location= JSONField(default=dict, null=True, blank=True)

    def set_location(self, x, y):
        self.class_location = {"x": x, "y": y}
        self.save()
    
    def get_location(self):
        return self.class_location.get("x"), self.class_location.get("y")

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['building', 'name'], name='unique_class_per_block')
        ]
    
    def __str__(self):
        return f"{self.name}"

class Hours(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.CharField(default="", null=False, choices=DAYS)
    order = models.CharField(default="", max_length=2)
    time_start = models.TimeField()
    time_end = models.TimeField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='hours')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['section', 'order'], name='unique_order_per_section')
        ]

    def __str__(self):
        return f"Hour {self.order}"