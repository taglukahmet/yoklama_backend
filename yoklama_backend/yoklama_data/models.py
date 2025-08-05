from django.db import models
from lecturer_data.models import Section, Hours
from student_data.models import Student
import uuid

class StudentList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name='student_list')
    students = models.ManyToManyField(Student, related_name='enrolled_lists')

    def __str__(self):
        return f"{self.section.lecture.name} {self.section.lecture.code} Section-{self.section.section_number} Student List"

class AttendanceList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_list = models.ForeignKey(StudentList, on_delete=models.CASCADE, related_name='attendance_lists')
    hour = models.ForeignKey(Hours, on_delete=models.CASCADE, related_name='attendance_lists')
    is_active= models.BooleanField(default=False)
    is_taken_rollcall= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} Dated {self.student_list.section.lecture.name} {self.student_list.section.lecture.code} Section-{self.student_list.section.section_number} Attendance List"
    
class AttendanceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendance_list = models.ForeignKey(AttendanceList, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    is_attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['attendance_list', 'student'], name='unique_list_per_student')
        ]
    
    def __str__(self):
        return f"{'Present' if self.attended else 'Absent'}"




