from django.views.generic import ListView

from inventory.models import InventoryItem


class VendorInventoryView(ListView):
    """
    Generic ListView for Vendor basic inventory page
    """
    queryset = InventoryItem.objects.filter(active=True, vendor=self.vendor_uuid)

    def __init__(self, **kwargs):
        self.vendor_uuid = kwargs.get('vendor_uuid')
        super(VendorInventoryView, self).__init__(self)
