import json
import pytest

from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_create_user__no_optional_fields():
    user_data = {
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "Guy",
        "password": "password",
        "profile": {},
        "address": {}
    }
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_user__include_optional_fields_no_photo():
    user_data = {
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "Guy",
        "password": "password",
        "profile": {
            "dob": "1986-10-28",
            "phone": "+41524204242",
        },
        "address": {
            "address_line_1": "c/o Some Guy",
            "address_line_2": "123 Fake Street",
            "address_line_3": "Suite 456",
            "city": "New Bedford",
            "state": "MA",
            "zip_code": "02745"
        }
    }
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_user__bad_data__duplicate_email():
    user_data = {
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "Guy",
        "password": "password",
        "profile": {},
        "address": {}
    }
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    # Submit the same data again, this time it should error as that user already exists
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user__bad_data__bad_phone():
    user_data = {
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "Guy",
        "password": "password",
        "profile": {
            "dob": "1986-10-28",
            "phone": "1524204242",
        },
        "address": {}
    }
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(response.content) == {"profile":{"phone":["The phone number entered is not valid."]}}


@pytest.mark.django_db
def test_create_user__bad_data__bad_dob():
    user_data = {
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "Guy",
        "password": "password",
        "profile": {
            "dob": "10-28-1986",
            "phone": "+41524204242",
        },
        "address": {}
    }
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (json.loads(response.content) ==
            {'profile': {'dob': ['Date has wrong format. Use one of these formats instead: ''YYYY[-MM[-DD]].']}})


@pytest.mark.django_db
def test_create_user__bad_data__bad_zip():
    user_data = {
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "Guy",
        "password": "password",
        "profile": {},
        "address": {
            "address_line_1": "c/o Some Guy",
            "address_line_2": "123 Fake Street",
            "address_line_3": "Suite 456",
            "city": "New Bedford",
            "state": "MA",
            "zip_code": "123"
        }
    }
    response = client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(response.content) == {'address': {'zip_code': ['Entered value is not a valid US Zip Code']}}


@pytest.mark.django_db
def test_update_user(user_profile, user_address):
    from gray_merchant.models import User

    user = User.objects.get(email='feynman@caltech.edu')
    assert user.first_name == 'Richard'
    assert user.profile
    assert user.address

    user_data = {
        "email": "feynman@caltech.edu",
        "first_name": "Test",
        "last_name": "Guy",
        "profile": {},
        "address": {},
    }
    response = client.patch(
        '/api/users/{}/'.format(user.id), data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(email='feynman@caltech.edu')
    assert user.first_name == "Test"
    assert user.last_name == "Guy"


@pytest.mark.django_db
def test_update_user__address(user_profile, user_address):
    from gray_merchant.models import User

    user = User.objects.get(email='feynman@caltech.edu')
    assert user.first_name == 'Richard'
    assert user.profile
    assert user.address

    user_data = {
        "email": "feynman@caltech.edu",
        "profile": {},
        "address": {
            "address_line_1": "c/o Some Guy",
            "address_line_2": "123 Fake Street",
            "address_line_3": "Suite 456",
            "city": "New Bedford",
            "state": "MA",
            "zip_code": "02745"
        },
    }
    response = client.patch(
        '/api/users/{}/'.format(user.id), data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(email='feynman@caltech.edu')
    assert user.address.address_line_1 == "c/o Some Guy"
    assert user.address.zip_code == "02745"


@pytest.mark.django_db
def test_update_user__profile(user_profile, user_address):
    from gray_merchant.models import User
    from datetime import date

    user = User.objects.get(email='feynman@caltech.edu')
    assert user.first_name == 'Richard'
    assert user.profile
    assert user.address

    user_data = {
        "email": "feynman@caltech.edu",
        "profile": {
            "dob": "1986-10-28",
            "phone": "+41524204242",
        },
        "address": {},
    }
    response = client.patch(
        '/api/users/{}/'.format(user.id), data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(email='feynman@caltech.edu')
    assert user.profile.dob == date(year=1986, month=10, day=28)


@pytest.mark.django_db
def test_get_user(user_profile, user_address):
    from gray_merchant.models import User

    user = User.objects.get(email='feynman@caltech.edu')
    response = client.get('/api/users/{}/'.format(user.id))
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert data.get('email') == 'feynman@caltech.edu'
    assert data.get('profile')
    assert data.get('address')
