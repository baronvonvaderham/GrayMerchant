import pytest


@pytest.fixture
def api_rf():
    """
    A Django Rest Framework `APIRequestFactory` instance.
    """
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


###################################################################
# Fixtures: gray_merchant

@pytest.fixture
def create_user():
    """
    A function to create 'gray_merchant.User' instances
    """
    from gray_merchant.models import User

    def _create_user(**kwargs):
        return User.objects.create(**kwargs)
    return _create_user


@pytest.fixture
def user(create_user):
    """
    A 'gray_merchant.User' instance for a generic default user.
    """
    return create_user(
        email='feynman@caltech.edu',
        first_name='Richard',
        last_name='Feynman',
        password='password',
    )


@pytest.fixture
def create_superuser():
    """
    A function to create 'gray_merchant.User' instances with superuser privileges
    """
    from gray_merchant.models import User

    def _create_user(**kwargs):
        return User.objects.create_superuser(**kwargs)

    return _create_user


@pytest.fixture
def superuser(create_superuser):
    """
    A 'gray_merchant.User' instance for a generic default user with superuser privileges
    """
    return create_superuser(
        email='dubridge@caltech.edu',
        first_name='Lee',
        last_name='DuBridge',
        password='password',
    )


@pytest.fixture
def create_user_profile(user):
    """
    A function to create 'gray_merchant.UserProfile' instances
    """
    from datetime import date
    from gray_merchant.models import UserProfile

    feynman_dob = date(year=1918, month=5, day=11)
    test_phone = '+41524204242'

    def _create_user_profile(profile_user=user, dob=feynman_dob, phone=test_phone, photo=None, **kwargs):
        return UserProfile.objects.create(
            user=profile_user,
            dob=dob,
            phone=phone,
            photo=None,
            **kwargs
        )
    return _create_user_profile


@pytest.fixture
def user_profile(create_user_profile):
    """
    A 'gray_merchant.UserProfile' instance for a generic default user.
    """
    return create_user_profile()


@pytest.fixture
def create_vendor():
    """
    A function to create 'gray_merchant.Vendor' instances
    """
    from gray_merchant.models import Vendor

    test_phone = '+41524204242'

    def _create_vendor(name='Test Vendor', email='vendor@gmail.com', phone=test_phone, **kwargs):
        return Vendor.objects.create(name=name, email=email, phone=phone, **kwargs)
    return _create_vendor


@pytest.fixture
def vendor(create_vendor):
    """
    A 'gray_merchant.Vendor' instance for a generic default vendor.
    """
    return create_vendor()


@pytest.fixture
def create_owner():
    """
    A function to create 'gray_merchant.Owner' instances
    """
    from gray_merchant.models import Owner

    def _create_owner(profile, vendor):
        return Owner.objects.create(profile=profile, vendor=vendor)
    return _create_owner


@pytest.fixture
def owner(user_profile, vendor, create_owner):
    """
    A 'gray_merchant.Owner' instance for a generic default owner from the
    default user profile and vendor objects.
    """
    return create_owner(profile=user_profile, vendor=vendor)


@pytest.fixture
def create_employee():
    """
    A function to create 'gray_merchant.Employee' instances
    """
    from gray_merchant.models import Employee

    def _create_owner(profile, vendor):
        return Employee.objects.create(profile=profile, vendor=vendor)

    return _create_owner


@pytest.fixture
def employee(user_profile, vendor, create_employee):
    """
    A 'gray_merchant.Employee' instance for a generic default employee from the
    default user profile and vendor objects.
    """
    return create_employee(profile=user_profile, vendor=vendor)


@pytest.fixture
def create_user_address():
    """
    A function to create 'gray_merchant.UserAddress' instances
    """
    from gray_merchant.models import UserAddress
    
    add_1 = '123 Fake Street'
    add_2 = 'Apt 456'
    city = 'Melbourne'
    state = 'FL'
    zip_code = 32901
    
    def _create_user_address(user):
        return UserAddress.objects.create(user=user,
                                          address_line_1=add_1,
                                          address_line_2=add_2,
                                          city=city,
                                          state=state,
                                          zip_code=zip_code)

    return _create_user_address


@pytest.fixture
def user_address(create_user_address, user):
    """
    A 'gray_merchant.UserAddress' instance for a generic User profile
    """
    return create_user_address(user=user)


@pytest.fixture
def create_vendor_address():
    """
    A function to create 'gray_merchant.VendorAddress' instances
    """
    from gray_merchant.models import VendorAddress

    add_1 = '123 Fake Street'
    add_2 = 'Apt 456'
    city = 'Melbourne'
    state = 'FL'
    zip_code = 32901

    def _create_vendor_address(vendor):
        return VendorAddress.objects.create(vendor=vendor,
                                            address_line_1=add_1,
                                            address_line_2=add_2,
                                            city=city,
                                            state=state,
                                            zip_code=zip_code)

    return _create_vendor_address


@pytest.fixture
def vendor_address(create_vendor_address, vendor):
    """
    A 'gray_merchant.vendorAddress' instance for a generic Vendor profile
    """
    return create_vendor_address(vendor=vendor)

###################################################################
# Fixtures: inventory

