import jwt
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings

def generate_qr_token(attendance_list_id, classroom_location):
    payload = {
        "classroom_location": dict(classroom_location),
        "attendance_list_id": str(attendance_list_id),
        "iat": timezone.now(),
        "exp": timezone.now() + timedelta(seconds=5),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


