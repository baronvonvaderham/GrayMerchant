import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import USStateField
from phonenumber_field.modelfields import PhoneNumberField

from .utils import ZipCodeValidator


class User(AbstractUser):
    """
    Custom User model extending the django base model
    """
    phone = PhoneNumberField()
    USERNAME_FIELD = 'email'


class Vendor(models.Model):
    """
    Class to contain the Vendor (store) information
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    email = models.EmailField(db_index=True)
    address = models.ForeignKey('Address', null=True, on_delete=models.SET_NULL)
    phone = PhoneNumberField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        return self.name


class Owner(models.Model):
    """
    Class to contain the Vendor Owner information
    """
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE,
                               related_name='owners', related_query_name='owner')

    class Meta:
        verbose_name = _('owner')
        verbose_name_plural = _('owners')

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Employee(models.Model):
    """
    Class to contain the Employee information
    """
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE,
                               related_name='employees', related_query_name='employee')

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Address(models.Model):
    """
    Class to contain Addresses
    """
    name = models.CharField(max_length=128)
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128, null=True, blank=True)
    address_line_3 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128)
    state = USStateField()
    zip_code = models.CharField(max_length=5, validators=[ZipCodeValidator])

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return self.address_line_1
