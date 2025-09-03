from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest

class AuthenticatedHttpRequest(HttpRequest):
    user: AbstractUser
