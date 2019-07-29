from rest_framework import serializers

from inventory.models import InventoryItem, GradingDetails


class GradingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradingDetails
        fields = ('grading_service', 'serial_number', 'overall_grade', 'autograph_grade',
                  'centering_grade', 'corners_grade', 'edges_grade', 'surfaces_grade',)


class InventoryItemSerializer(serializers.ModelSerializer):
    grading_details = GradingDetailsSerializer(required=False)

    class Meta:
        model = InventoryItem
        fields = ('name', 'description', 'card', 'vendor', 'condition', 'is_foil',
                  'list_price_override', 'buylist_price_override', 'active', 'grading_details')
