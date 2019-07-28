from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'token-auth/$', obtain_jwt_token, name="obtain-jwt-token")
]
