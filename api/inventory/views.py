from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from gray_merchant.models import Vendor, UserProfile
from inventory.models import InventoryItem, GradingDetails

from .serializers import InventoryItemSerializer


class InventoryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    A viewset for interacting with a Vendor's Inventory objects
    """
    def list(self, request):
        profile = request.user.profile
        owner = None
        employee = None

        # Try to get the owner or employee object associated with the authenticated user making the request
        try:
            owner = profile.owner
        except AttributeError:
            try:
                employee = profile.employee
            except AttributeError:
                return Response(status=status.HTTP_403_FORBIDDEN, data="User is not an owner or employee of any Vendor")

        # Try to get the vendor from the UUID supplied in the URL
        uuid = self.kwargs.get('pk')
        vendor = Vendor.objects.filter(uuid=uuid).first()
        if not vendor:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="No such Vendor with UUID {}".format(uuid))

        # If you found both, great! Now check that the employee/owner matches the vendor
        authorized_vendor = owner.vendor if owner else employee.vendor
        if vendor != authorized_vendor:
            return Response(status=status.HTTP_403_FORBIDDEN, data="User not authorized to access this Vendor")

        # If you got this far, everything looks great, let's grab that inventory data
        queryset = InventoryItem.objects.filter(vendor=authorized_vendor, active=True)
        serializer = InventoryItemSerializer(queryset, many=True)
        return Response(serializer.data)
