from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from api.views import UserViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'token-auth/$', obtain_jwt_token, name="obtain-jwt-token"),
]
