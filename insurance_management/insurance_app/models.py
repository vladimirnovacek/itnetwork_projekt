from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house_number = models.IntegerField(null=True, blank=True)
    building_id_number = models.IntegerField()
    postal_code = models.CharField(max_length=8)

    def __str__(self):
        number = str(self.building_id_number)
        if self.house_number:
            number += f"/{self.house_number}"
        return f"{self.street} {number}, {self.postal_code} {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "Addresses"


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.IntegerField()
    email = models.CharField(max_length=256, unique=True, db_index=True)
    id_domicile = models.ForeignKey(to=Address, on_delete=models.RESTRICT, related_name="domicile")
    id_mailing_address = models.ForeignKey(to=Address, on_delete=models.RESTRICT, related_name="mailing_address")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    annual_price = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: {self.description}"


class Insurance(models.Model):
    id_insured = models.ForeignKey(to=User, on_delete=models.RESTRICT, related_name="insured")
    id_policyholder = models.ForeignKey(to=User, on_delete=models.RESTRICT, related_name="policyholder")
    id_product = models.ForeignKey(to=Product, on_delete=models.RESTRICT)
    payment = models.IntegerField()
    conclusion_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_product.name} ze dne {self.conclusion_date}, " \
               f"pojistník {self.id_insured}"


class Insured_event(models.Model):
    id_insurance = models.ForeignKey(to=Insurance, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
    approved = models.BooleanField(default=False)
    payout = models.IntegerField(default=0)

    def __str__(self):
        return f"Pojistná událost ke smlouvě {self.id_insurance}"
