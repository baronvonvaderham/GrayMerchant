import uuid

from django.db import models

from card_catalog.models import Card
from transactions.models import Purchase, Sale


class InventoryItem(models.Model):
    """
    Class to contain the items entered into a vendor's inventory.
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=256, blank=True)
    description = models.TextField()
    card = models.ForeignKey(Card, null=True, blank=True, on_delete=models.SET_NULL)
    selling_price = models.FloatField(null=True, blank=True)
    buylist_price = models.FloatField(null=True, blank=True)
    purchase_transaction = models.ForeignKey(Purchase, null=True, blank=True, on_delete=models.SET_NULL)
    sale_transaction = models.ForeignKey(Sale, null=True, blank=True, on_delete=models.SET_NULL)
