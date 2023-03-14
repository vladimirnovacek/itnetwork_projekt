"""
Module for defining own authentication backends.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest


class EmailBackend(ModelBackend):
    """
    Backend allowing authentication via e-mail address and password
    """
    def authenticate(self, request: HttpRequest, username: str = None, password: str = None, **kwargs):
        """
        Authentication method. If authenticated, returns user instance, otherwise returns None
        :param HttpRequest request:
        :param str username:
        :param str password:
        :param kwargs:
        :return AbstractBaseUser | None:
        """
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except Exception as e:
            raise e
        else:
            if user.check_password(password):
                return user
        return None
