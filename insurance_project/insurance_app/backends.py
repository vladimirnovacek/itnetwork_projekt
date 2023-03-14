"""
Module for defining own authentication backends.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from insurance_app.models import Person


class EmailBackend(ModelBackend):
    """
    Backend allowing authentication via e-mail address and password
    """
    def authenticate(self, request: HttpRequest, email: str = None, password: str = None, **kwargs):
        """
        Authentication method. If authenticated, returns user instance, otherwise returns None
        :param HttpRequest request:
        :param str email:
        :param str password:
        :param kwargs:
        :return AbstractBaseUser | None:
        """
        user_model = get_user_model()
        user = user_model.objects.get(email=email)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
