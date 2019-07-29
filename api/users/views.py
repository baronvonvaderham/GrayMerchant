from rest_framework import viewsets, permissions

from api.users.serializers import UserSerializer
from gray_merchant.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
