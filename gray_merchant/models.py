import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import USStateField
from phonenumber_field.modelfields import PhoneNumberField

from .utils import ZipCodeValidator


class CustomUserManager(BaseUserManager):
    """
    A custom user manager to deal with email as a unique identifier for auth
    instead of usernames.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Must provide an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model extending the django base model
    """
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=64)
    last_name = models.CharField(_('last name'), max_length=64)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return "{} : {} {}".format(self.email, self.first_name, self.last_name)


class UserProfile(models.Model):
    """
    A class to contain additional user data so as not to clutter up the user model
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', primary_key=True
    )
    dob = models.DateField(_('date of birth'), null=True, blank=True)
    phone = PhoneNumberField(_('phone number'), null=True, blank=True)
    photo = models.ImageField(_('photo'), upload_to='profile_images', null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


class Vendor(models.Model):
    """
    Class to contain the Vendor (store) information
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(_('name'), max_length=128, unique=True)
    email = models.EmailField(_('email'), db_index=True)
    phone = PhoneNumberField(_('phone'))
    is_active = models.BooleanField(_('active'), default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        return self.name


class Owner(models.Model):
    """
    Class to contain the Vendor Owner information
    """
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE,
                               related_name='owners', related_query_name='owner')

    objects = models.Manager()

    class Meta:
        verbose_name = _('owner')
        verbose_name_plural = _('owners')


class Employee(models.Model):
    """
    Class to contain the Employee information
    """
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE,
                               related_name='employees', related_query_name='employee')

    objects = models.Manager()

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')


class UserAddress(models.Model):
    """
    Class to contain Addresses for Users
    """
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='address')
    address_line_1 = models.CharField(_('address line 1'), max_length=128, null=True, blank=True)
    address_line_2 = models.CharField(_('address line 2'), max_length=128, null=True, blank=True)
    address_line_3 = models.CharField(_('address line 3'), max_length=128, null=True, blank=True)
    city = models.CharField(_('city'), max_length=128, null=True, blank=True)
    state = USStateField(_('state'), null=True, blank=True)
    zip_code = models.CharField(_('zip code'), max_length=5, validators=[ZipCodeValidator], null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return self.address_line_1


class VendorAddress(models.Model):
    """
    Class to contain Addresses for Vendors
    """
    vendor = models.OneToOneField(Vendor, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='address')
    company_name = models.CharField(_('name'), max_length=128)
    address_line_1 = models.CharField(_('address line 1'), max_length=128)
    address_line_2 = models.CharField(_('address line 2'), max_length=128, null=True, blank=True)
    address_line_3 = models.CharField(_('address line 3'), max_length=128, null=True, blank=True)
    city = models.CharField(_('city'), max_length=128)
    state = USStateField(_('state'))
    zip_code = models.CharField(_('zip code'), max_length=5, validators=[ZipCodeValidator])

    objects = models.Manager()

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return self.address_line_1
