from django.contrib.auth.backends import ModelBackend
from .models import Users


class PasswordlessAuth(ModelBackend):
    def authenticate(self, request, username):
        try:
            user = Users.objects.get(email=username)
            return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Users.objects.get(pk=user_id)
            return user 
        except Users.DoesNotExist:
            return None  