from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    id_number = models.CharField(max_length=250)


class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    address_type_choices = (
        (0, "Physical"),
        (1, "Postal"),
    )
    address_type = models.IntegerField(
        choices=address_type_choices,
        default=0,
    )
    street = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
    )
    street_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    unit_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    building = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    area = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    province = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )
