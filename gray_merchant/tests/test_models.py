import pytest


@pytest.mark.django_db
def test_user(user_profile):
    from datetime import date
    from gray_merchant.models import User

    user = User.objects.get(email='feynman@caltech.edu')
    assert user.profile.dob == date(year=1918, month=5, day=11)
    assert user.profile.phone == '+41524204242'


@pytest.mark.django_db
def test_superuser(superuser):
    from gray_merchant.models import User

    user = User.objects.get(email='dubridge@caltech.edu')
    assert user.is_superuser


@pytest.mark.django_db
def test_vendor(vendor):
    from gray_merchant.models import Vendor

    get_vendor = Vendor.objects.get(name='Test Vendor')
    assert get_vendor.email == 'vendor@gmail.com'
    assert get_vendor.phone == '+41524204242'


@pytest.mark.django_db
def test_owner(owner):
    from gray_merchant.models import Vendor

    get_vendor = Vendor.objects.get(name='Test Vendor')
    assert get_vendor.owners.first() == owner


@pytest.mark.django_db
def test_employee(employee):
    from gray_merchant.models import Vendor

    get_vendor = Vendor.objects.get(name='Test Vendor')
    assert get_vendor.employees.first() == employee


@pytest.mark.django_db
def test_user_address(user_address):
    from gray_merchant.models import User

    get_user = User.objects.get(email='feynman@caltech.edu')
    assert get_user.address == user_address


@pytest.mark.django_db
def test_vendor_address(vendor_address):
    from gray_merchant.models import Vendor

    get_vendor = Vendor.objects.get(email='vendor@gmail.com')
    assert get_vendor.address == vendor_address
