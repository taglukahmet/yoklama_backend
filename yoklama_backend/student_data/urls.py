from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path('students/department/<uuid:department_id>/', StudentofDepartmentView.as_view(), name='get_post_students_of_a_department'),
    path('students/<uuid:student_id>/', StudentonlyView.as_view(), name='get_put_student'),
    path('students/login/', CustomTokenObtainPairView.as_view(), name='student_login'),
    path('students/login/refresh', TokenRefreshView.as_view(), name='student_login_refresh'),
    path('students/lectures/<uuid:student_id>/', StudentLecturesView.as_view(), name='get_students_enrolled_courses')


]