from django.db import models
from lecturer_data.models import Section, Hours
from student_data.models import Student
# Create your models here.

class StudentList(models.Model):
    name = models.CharField(max_length=100)
    section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name='student_list')
    students = models.ManyToManyField(Student, related_name='enrolled_lists')

    def __str__(self):
        return f"{self.section.lecture.full_name} Section-{self.section.section_number} Student List"

class AttendanceList(models.Model):
    student_list = models.ForeignKey(StudentList, on_delete=models.CASCADE, related_name='attendance_lists')
    hour = models.OneToOneField(Hours, on_delete=models.CASCADE, related_name='attendance_list')
    attendance_date = models.DateTimeField(auto_now_add=True)
    is_active= models.BooleanField(default=False)
    is_taken_rollcall= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attendance_date} Dated {self.student_list.section.lecture.full_name} Section-{self.student_list.section.section_number} Attendance List"
    
class AttendanceRecord(models.Model):
    attendance_list = models.ForeignKey(AttendanceList, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['attendance_list', 'student'], name='unique_list_per_student')
        ]
    
    def __str__(self):
        return f"{'Present' if self.attended else 'Absent'}"




