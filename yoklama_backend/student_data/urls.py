from django.urls import path
from .views import StudentView


urlpatterns = [
    path('1', StudentView.as_view()),
]