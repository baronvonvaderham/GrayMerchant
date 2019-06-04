from django.conf.urls import url

from .views import VendorInventoryView

urlpatterns = [
    url(r'^inventory/', VendorInventoryView.as_view(), name='vendor-inventory')
]
