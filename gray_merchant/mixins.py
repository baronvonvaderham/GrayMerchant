from django.http import Http404

from .models import Vendor, Owner, Employee


class VendorPermissionMixin(object):

    def has_permission(self, user, vendor_uuid):
        try:
            vendor = Vendor.objects.get(uuid=vendor_uuid)
        except Vendor.DoesNotExist:
            return False
        employee = Employee.objects.filter(user=user).first()
        owner = Owner.objects.filter(user=user).first()
        if employee:
            return employee.vendor == vendor
        elif owner:
            return owner.vendor == vendor

    def dispatch(self, request, *args, **kwargs):

        if not self.has_permission(user=request.user, vendor_uuid=kwargs.get('vendor_uuid')):
            raise Http404('You do not have permission to access this vendor.')
        return super(VendorPermissionMixin, self).dispatch(request, *args, **kwargs)
