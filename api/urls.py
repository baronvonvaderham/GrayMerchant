from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from api.inventory.views import InventoryViewSet
from api.users.views import UserViewSet

router = routers.DefaultRouter()

# router.register('inventory', InventoryViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'token-auth/$', obtain_jwt_token, name="obtain-jwt-token"),
]
