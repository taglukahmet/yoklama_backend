from django.db import models
from lecturer_data.models import Department
import uuid
from django.contrib.auth.models import User



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(default="", null=False, max_length=100)
    last_name = models.CharField(default="", null=False, max_length=100)  
    department= models.ForeignKey(Department, on_delete=models.CASCADE, related_name='enrolled_students')
    year= models.CharField(max_length=2)
    student_number= models.CharField(default="", max_length=15)
    
    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['department', 'student_number'], name='unique_number_per_dept')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
