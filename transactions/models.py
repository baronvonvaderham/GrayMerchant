import datetime
import uuid

from django.db import models

from card_catalog.models import CardPrice
from gray_merchant.models import User


class BaseTransaction(models.Model):
    """
    SuperClass for all Transaction models' common attributes
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Purchase(BaseTransaction):
    """
    Class to contain Purchase transactions (def: vendor buying item from customer)
    """
    purchase_price = models.FloatField(null=True, blank=True)
    retail_price_data = models.ForeignKey(CardPrice, null=True, blank=True, on_delete=models.SET_NULL)


class Sale(BaseTransaction):
    """
    Class to contain Sale transactions (def: vendor selling item to customer)
    """
    sale_price = models.FloatField(null=True, blank=True)
