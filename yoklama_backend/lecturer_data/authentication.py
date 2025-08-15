import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Lecturer
from yoklama_backend.settings import API_CBU_DOMAIN, CBU_DOMAIN

class APILoginBackend(BaseBackend):

    def authenticate(self, request, username = None, password = None):
        try:
            domain = username.split('@')[1]
        except (IndexError, AttributeError):
            return None
        
        if domain.lower() != CBU_DOMAIN:
            return None
        
        try:
            api_endpoint = API_CBU_DOMAIN
            response = request.post(api_endpoint, json={'username':username, 'password':password})

            response.raise_for_status()
            api_data = response.json()
        except requests.RequestException:
            return None
        
