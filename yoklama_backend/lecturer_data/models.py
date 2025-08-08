from django.db import models
from django.utils import timezone
from django.db.models import JSONField, Q
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# For every model we use UUID, then we keep it clean, precise and unique
# Order of data in the models are not important in here, its all the same

# University and the academic calender info
class University(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100, unique=True)
    academic_calendar_dates= models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name}"

# Faculty and university info with a Foreignkey
class Faculty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')

    def __str__(self):
        return f"{self.name}"

# Departmnent and faculty info with a Foreignkey
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="", null=False, max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name}"

# Lecturer info, conneted to the department with a Foreignkey and tied to a user with an OnetOnefield
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(default="", null=True, blank=True, max_length=30)
    first_name = models.CharField(default="", null=True, blank=True, max_length=100)
    last_name = models.CharField(default="", null=True, blank=True, max_length=100) 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturers')
    phone = PhoneNumberField(null=True, blank=True, region='TR')
    #not really tested yet
    profile_photo = models.ImageField(upload_to='lecturer_photos/', null=True, blank=True) 
    # Created_at may be used in the future, delete it if it remains redundant
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

# Lecture info, connected to a department with a Foreignkey
class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="", null=False, max_length=6)
    code = models.CharField(default="", null=False, max_length=6)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lectures')
    # thats the actual name of the lecture
    explicit_name = models.CharField(default="", null=True, blank=True, max_length=100)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['code', 'department'], name='unique_code_per_department')
        ]
    
    def __str__(self):
        return f"{self.name} {self.code}"

# Section info, connected to a lecture and a lecturer with a Foreignkey
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
        return f"{self.lecture.name} {self.lecture.code} Section-{self.section_number}"

# Building info, connected to a department with a Foreignkey, it doesnt have to be a department building therefore faculty and uni info also added
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

# Classroom info, connected to a building with a Foreignkey
class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(default="", null=False, max_length=100)
    building= models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classes')
    # this location is for future use
    class_location= JSONField(default=dict, null=True, blank=True)
    #these functions are for backend use, not for frontend
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

# Hour of a section's info, connected to a classroom and a section with a Foreignkey
class Hours(models.Model):
    # All the day options for consistency, they are duplicate, it must be one for the database one for the usage
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # the day of the week
    day = models.CharField(default="", null=False, choices=DAYS)
    # first, second maybe third hour of a section
    order = models.CharField(default="", max_length=2)
    # the format is Hour:Minute:Seconds.miliseconds you can just enter 09:40 and it gets the rest
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