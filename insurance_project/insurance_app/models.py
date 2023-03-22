"""
Module containing models for this app
"""
import unicodedata
from typing import Any

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
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list = ["first_name", "last_name", "date_of_birth"]  # other fields are not required for staff

    objects: BaseUserManager = PersonManager()

    first_name: models.Field = models.CharField(max_length=150, verbose_name='Křestní jméno')
    last_name: models.Field = models.CharField(max_length=150, verbose_name='Příjmení')
    email: models.Field = models.EmailField(unique=True, verbose_name='E-mail')
    phone: models.Field = modelfields.PhoneNumberField(region="CZ", null=True, verbose_name='Telefon')
    address1: models.Field = models.CharField(max_length=150, default="", verbose_name='Adresa')
    address2: models.Field = models.CharField(max_length=150, blank=True, default="", verbose_name='Adresa - druhý řádek')
    postal_code: models.Field = models.CharField(max_length=12, default="", verbose_name='PSČ')
    city: models.Field = models.CharField(max_length=150, default="", verbose_name='Město')
    country: models.Field = models.CharField(max_length=150, default="", verbose_name='Stát')
    date_of_birth: models.Field = models.DateField(verbose_name='Datum narození')
    is_staff: models.Field = models.BooleanField(default=False, verbose_name='Zaměstnanec')
    is_superuser: models.Field = models.BooleanField(default=False, verbose_name='Administrátor')
    slug: models.Field = models.SlugField(unique=True, null=False)

    @property
    def full_address(self) -> str:
        chunks = tuple(
            filter(
                lambda c: c,
                (
                    str(self.address1),
                    str(self.address2),
                    str(self.city),
                    str(self.postal_code),
                    str(self.country)
                )
            )
        )
        return ", ".join(chunks)

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

    def save(
        self, force_insert: bool = False, force_update: bool = False, using: Any = None, update_fields: Any = None
    ):
        super().save(force_insert, force_update, using, update_fields)
        if not self.slug:
            self.slug = self._generate_slug()
        super().save(force_insert, force_update, using, update_fields)

    def _generate_slug(self) -> str:
        """
        Returns an object slug
        :return:
        """
        last_name = self._remove_interpunction(str(self.last_name)).lower()
        first_name = self._remove_interpunction(str(self.first_name)).lower()
        return f"{self.pk}-{last_name}-{first_name}"

    def _remove_interpunction(self, text: str) -> str:
        """
        Transforms a text to ascii.
        :param text:
        :return:
        """
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode('utf-8')

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Product(models.Model):
    """
    Model represents an insurance product. It doesn't represent a particular contract.
    """
    name: models.Field = models.CharField(max_length=64, unique=True, verbose_name='Název')
    description: models.Field = models.TextField(default="", verbose_name='Popis')
    active: models.Field = models.BooleanField(default=True, blank=True, verbose_name='Aktivní')
    image: models.Field = models.ImageField(upload_to='images/', verbose_name='Obrázek')

    def __str__(self) -> str:
        inactive = " (nedostupné)" if not self.active else ""
        return str(self.name) + inactive

    class Meta:
        verbose_name = u'Produkt'


class Contract(models.Model):
    """
    Model represents a particular contract
    """
    objects: models.Manager
    product: models.Field = models.ForeignKey(to=Product, on_delete=models.RESTRICT, verbose_name='Produkt')
    insured: models.Field = models.ForeignKey(to=Person, on_delete=models.RESTRICT, verbose_name='Pojištěnec')
    conclusion_date: models.Field = models.DateField(auto_now_add=True, verbose_name='Datum uzavření')
    payment: models.Field = models.PositiveIntegerField(verbose_name='Pravidelná platba')

    @property
    def contract_number(self) -> int:
        """
        Simple non-random simulation of a unique contract number with 8 - 10 digits. It is based on primary key.
        :return int:
        """
        return 10_000_001 + self.pk * 127 ** 2

    @classmethod
    def get_object_by_contract_number(cls, contract_number: int) -> int:
        """
        Returns an object identified by a contract number
        :param contract_number:
        :return:
        """
        return cls.objects.get(pk=cls.get_pk_by_contract_number(contract_number))

    @staticmethod
    def get_pk_by_contract_number(contract_number: int) -> int:
        """
        Returns a primary key of a contract identified by a contract number.
        :param int contract_number:
        :return int:
        """
        return int((contract_number - 10_000_001) / (127 ** 2))

    def __str__(self):
        return f"{self.product} číslo {self.contract_number}"


class InsuredEvent(models.Model):
    """
    Model for insured event
    """
    contract: Contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE, verbose_name='Smlouva')
    event_date: models.DateField = models.DateField(verbose_name='Datum události')
    reporting_date: models.DateField = models.DateField(auto_now_add=True)
    description: models.TextField = models.TextField(verbose_name='Popis události')
    processed: models.BooleanField = models.BooleanField(default=False, verbose_name='Zpracováno')
    approved: models.BooleanField = models.BooleanField(default=False, verbose_name='Schváleno')
    payout: models.IntegerField = models.IntegerField(null=True, blank=True, verbose_name='Pojistné plnění')

    @property
    def client(self):
        return self.contract.insured

    def __str__(self):
        return f'Pojistná událost č. {self.pk} ke smlouvě {self.contract}'
