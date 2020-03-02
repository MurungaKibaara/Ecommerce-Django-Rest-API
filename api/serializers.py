from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'product_description', 'product_quantity', 'product_price')


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

class OrderSerializer(serializers.ModelSerializer):
    order_status = ChoiceField(choices=Order.STATUS)
    product_id = serializers.RelatedField(source='Product', read_only=True)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'product_id',
            'order_quantity',
            'payment',
            'order_date',
            'order_status',
            'delivery_date'
            )
