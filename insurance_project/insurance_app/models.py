from django.contrib.auth.models import User
from django.db import models

from phonenumber_field import modelfields


class Person(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone = modelfields.PhoneNumberField(region="CZ")
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True, default="")
    postal_code = models.CharField(max_length=12)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user} detail"


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
