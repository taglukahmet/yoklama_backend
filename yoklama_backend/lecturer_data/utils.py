from django.contrib.auth.models import User
from .models import Lecturer



def create_lecturer_with_user(username, password, first_name, last_name, email, **kwargs):
    user = User.objects.create_user(
        # username= username,   this place will be decided upon
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    lecturer = Lecturer.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        **kwargs
    )
    return lecturer