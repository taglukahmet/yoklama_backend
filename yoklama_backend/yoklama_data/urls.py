from django.urls import path
from .views import *


urlpatterns = [

    path('student_list/<uuid:section_id>/', StudentListView.as_view(), name='get_post_put_student_list'),
    path('attendance_list/hour/<uuid:hour_id>/', AttendanceListofHourView.as_view(), name='get_post_put_attendance_list'),
    path('attendance_list/student_list/<uuid:student_list_id>/', AttendanceListofStudentListView.as_view(), name='get_post_put_attendance_list'),
    path('attendance_records/attendance_list/<uuid:attendance_list_id>/', AttendanceRecordofAttendanceListView.as_view(), name='get_post_put_attendance_list'),
    path('attendance_records/<uuid:attendance_record_id>/', AttendanceRecordOnlyView.as_view(), name='get_post_put_attendance_list')

]