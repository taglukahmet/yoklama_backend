from django.urls import path
from .views import *

urlpatterns = [
    path('qr_token/<uuid:attendance_list_id>/', QRTokenView.as_view(), name='qr_token_send'),
    path('qr_validate/', ValidateAttendanceView.as_view(), name='validate_attendance')
]