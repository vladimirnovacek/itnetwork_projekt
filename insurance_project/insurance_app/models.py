from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models

from phonenumber_field import modelfields


class Person(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = modelfields.PhoneNumberField(region="CZ")
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True, default="")
    postal_code = models.CharField(max_length=12)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=False)

    @property
    def full_address(self):
        return ", ".join((
            str(self.address1),
            str(self.address2),
            str(self.city),
            str(self.postal_code),
            str(self.country)
        ))

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = self._get_slug()
        return super().save(force_insert, force_update, using, update_fields)

    def _get_slug(self):
        return f"{self.pk}-{self.last_name}-{self.first_name}"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except Exception as e:
            raise e
        else:
            if user.check_password(password):
                return user
        return None


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(default="")
    active = models.BooleanField(default=True)

    def __str__(self):
        inactive = " (nedostupné)" if not self.active else ""
        return str(self.name) + inactive


class Contract(models.Model):
    objects: models.Manager
    product = models.ForeignKey(to=Product, on_delete=models.RESTRICT)
    insured = models.ForeignKey(to=User, on_delete=models.RESTRICT)
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
