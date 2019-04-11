import datetime
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from card_catalog.models import CardPrice
from gray_merchant.models import User
from inventory.models import InventoryItem


class TransactionItem(models.Model):
    """
    Class to contain for all Transaction Items for all Transactions
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    card = models.ForeignKey(InventoryItem, null=True, on_delete=models.SET_NULL)
    notes = models.TextField()
    captured_price = models.ForeignKey(CardPrice, null=True, on_delete=models.SET_NULL,
                                       help_text=_("Most recent price synced for item at time of transaction"))

    class Meta:
        verbose_name = _('transaction_item')
        verbose_name_plural = _('transaction_items')

    def __str__(self):
        price = self.captured_price.foil_market if self.card.is_foil else self.captured_price.market
        return "{} {} - ${}".format(self.card.condition, self.card.name, price)


class BaseTransaction(models.Model):
    """
    SuperClass for all Transaction models' common attributes and methods
    """
    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('store_credit', 'Store Credit'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal')
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPE_CHOICES)
    transaction_total = models.FloatField(help_text=_("Total amount of transaction."))
    notes = models.TextField()


class Purchase(BaseTransaction):
    """
    Class to contain Purchase transactions (def: vendor buying item from customer)
    """
    buylist_items = models.ManyToManyField(TransactionItem, related_name='buylist_items')

    class Meta:
        verbose_name = _('purchase_transaction')
        verbose_name_plural = _('purchase_transactions')


class Sale(BaseTransaction):
    """
    Class to contain Sale transactions (def: vendor selling item to customer)
    """
    sold_items = models.ManyToManyField(TransactionItem, related_name='sold_items')

    class Meta:
        verbose_name = _('sale_transactions')
        verbose_name_plural = _('sale_transactions')
