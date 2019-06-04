from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .mixins import VendorPermissionMixin
from inventory.models import InventoryItem


class VendorInventoryView(LoginRequiredMixin, VendorPermissionMixin, ListView):
    """
    Generic ListView for Vendor basic inventory page
    """
    model = InventoryItem
    template_name = 'vendor_inventory.html'

    def get_queryset(self):
        qs = super(VendorInventoryView, self).get_queryset()
        return qs.filter(vendor__id=self.kwargs['vendor_id'])
