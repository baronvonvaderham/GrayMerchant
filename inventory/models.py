import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class InventoryItem(models.Model):
    """
    Class to contain the items entered into a vendor's inventory.
    """

    CONDITION_CHOICES = (
        ('M', 'Mint'),
        ('NM', 'Near Mint'),
        ('LP', 'Lightly Played'),
        ('MP', 'Moderately Played'),
        ('HP', 'Heavily Played'),
        ('DMG', 'Damaged')
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    card = models.ForeignKey('card_catalog.Card', null=True, blank=True, on_delete=models.SET_NULL, db_index=True)
    vendor = models.ForeignKey('gray_merchant.Vendor', null=True, blank=True, on_delete=models.SET_NULL, db_index=True)
    condition = models.CharField(max_length=3, choices=CONDITION_CHOICES, help_text="Card condition")
    grading_details = models.ForeignKey('GradingDetails',null=True, on_delete=models.SET_NULL)
    is_foil = models.BooleanField(default=False, help_text="Is the card foil?")
    list_price_override = models.FloatField(null=True, blank=True,
                                            help_text=_("Manually set list price to override "
                                                        "automatic value from TCGPlayer data"))
    buylist_price_override = models.FloatField(null=True, blank=True,
                                               help_text=_("Manually set buylist price to override "
                                                           "automatic value from TCGPlayer data"))
    purchase_transaction = models.ForeignKey('transactions.Purchase', null=True, blank=True, on_delete=models.SET_NULL,
                                             related_name='purchase_items',
                                             help_text=_("Purchase transaction in which item was acquired"))
    sale_transaction = models.ForeignKey('transactions.Sale', null=True, blank=True, on_delete=models.SET_NULL,
                                         related_name='sale_items',
                                         help_text=_("Sale transaction in which item was sold"))
    active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('inventory_item')
        verbose_name_plural = _('inventory_items')

    def __str__(self):
        return self.name


class GradingDetails(models.Model):
    """
    Class to contain details for graded cards entered into inventory
    """

    GRADING_SERVICES = (
        ('BGS', 'Beckett Grading Services'),
        ('BAS', 'Beckett Authentication Services'),
        ('PSA', 'Professional Sports Authentication')
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    grading_service = models.CharField(max_length=32, choices=GRADING_SERVICES)
    serial_number = models.CharField(max_length=12)
    overall_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    autograph_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    centering_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    corners_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    edges_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    surfaces_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)

    objects = models.Manager()

    class Meta:
        verbose_name = _('grading_details')
