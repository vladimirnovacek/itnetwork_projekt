"""
Module for defining own authentication backends.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest


UserModel = get_user_model()


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
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel.objects.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user
