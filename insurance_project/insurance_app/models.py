"""
Module containing models for this app
"""
import unicodedata

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from phonenumber_field import modelfields


class PersonManager(BaseUserManager):
    """
    Manager for the class Person. Default manager can't be used for Person model authenticates via e-mail.
    """
    def _create_user(self, email: str, password: str, **extra_fields) -> AbstractBaseUser:
        """
        Create and save a user with the given email, and password.
        :param str email:
        :param str password:
        :param extra_fields:
        :return AbstractBaseUser:
        """
        if not email:
            raise ValueError("E-mail musí být zadán.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str = None, password: str = None, **extra_fields) -> AbstractBaseUser:
        """
        Create and save a user with the given email, and password.
        :param str email:
        :param str password:
        :param extra_fields:
        :return AbstractBaseUser:
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str = None, password: str = None, **extra_fields) -> AbstractBaseUser:
        """
        Create and save a superuser with the given email, and password.
        :param str email:
        :param str password:
        :param extra_fields:
        :return AbstractBaseUser:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Person(AbstractBaseUser, PermissionsMixin):
    """
    This model represents the users, both regular and admins.
    """
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth"]

    objects = PersonManager()

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = modelfields.PhoneNumberField(region="CZ", null=True)
    address1 = models.CharField(max_length=150, default="")
    address2 = models.CharField(max_length=150, blank=True, default="")
    postal_code = models.CharField(max_length=12, default="")
    city = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=150, default="")
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=False)

    @property
    def full_address(self):
        chunks = tuple(filter(lambda c: c, (self.address1, self.address2, self.city, self.postal_code, self.country)))
        return ", ".join(chunks)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        if not self.slug:
            self.slug = self._generate_slug()
        super().save(force_insert, force_update, using, update_fields)

    def _generate_slug(self):
        last_name = self._remove_interpunction(str(self.last_name)).lower()
        first_name = self._remove_interpunction(str(self.first_name)).lower()
        return f"{self.pk}-{last_name}-{first_name}"

    def _remove_interpunction(self, text: str):
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode('utf-8')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(default="")
    active = models.BooleanField(default=True, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        inactive = " (nedostupné)" if not self.active else ""
        return str(self.name) + inactive


class Contract(models.Model):
    objects: models.Manager
    product = models.ForeignKey(to=Product, on_delete=models.RESTRICT)
    insured = models.ForeignKey(to=Person, on_delete=models.RESTRICT)
    conclusion_date = models.DateTimeField(auto_now_add=True)
    payment = models.IntegerField()

    @property
    def contract_number(self) -> int:
        """
        Simple simulation of a unique contract number with 8 - 10 digits
        :return:
        """
        return 10_000_001 + self.pk * 127 ** 2

    @staticmethod
    def get_pk_by_contract_number(contract_number):
        return int((contract_number - 10_000_001) / (127 ** 2))

    def __str__(self):
        return f"{self.product}, klient: {self.insured}"


# class DeletedContract(Contract):
#     def __str__(self):
#         return super(DeletedContract, self).__str__() + "(zrušeno)"
