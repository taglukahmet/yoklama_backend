from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenRefreshView)


urlpatterns = [
    path('universities/', UniversityListView.as_view(), name='get_universities'),
    path('faculties/<uuid:university_id>/', FacultyListView.as_view(), name='get_faculties'),
    path('departments/<uuid:faculty_id>/', DepartmentListView.as_view(), name='get_departments'),
    path('lecturers/signup/', LecturerSignUpView.as_view(), name='lecturer_signup_post'),
    path('lecturers/<uuid:lecturer_id>/', LecturerProfileView.as_view(), name= 'lecturer_profile_view_edit'),
    path('buildings/<uuid:university_id>/', BuildingView.as_view(), name='get_buildings'),
    path('classrooms/<uuid:building_id>/', ClassroomView.as_view(), name='get_classrooms'),
    path('lectures/<uuid:department_id>/', LectureView.as_view(), name='get_lectures'),
    path('sections/lecture/<uuid:lecture_id>/', SectionofLectureView.as_view(), name='get_post_sections_of_a_lecture'),
    path('sections/<uuid:section_id>/', SectiononlyView.as_view(), name='get_put_sections'),
    path('hours/section/<uuid:section_id>/', HoursofSectionView.as_view(), name='get_post_hours_of_a_section'),
    path('hours/<uuid:hour_id>/', HouronlyView.as_view(), name='get_put_hours'),
    path('lecturers/login/', CustomTokenObtainPairView.as_view(), name='lecturer_login'),
    path('lecturers/login/refresh', TokenRefreshView.as_view(), name='lecturer_login_refresh'),
]