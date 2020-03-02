from rest_framework import serializers
from .models import Product, Order, Sale


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'product_description', 'product_quantity', 'product_price')

class OrderSerializer(serializers.ModelSerializer):
    order_status = ChoiceField(choices=Order.STATUS)
    product_id = ProductSerializer(source='Product', read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('order_id','product_id','order_quantity','order_date','order_status')


class SaleSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer(source='Order', many=True)

    class Meta:
        order = Sale
        fields = ('order_id','delivery_id','delivery_date' 'confirm_date','reference' )
