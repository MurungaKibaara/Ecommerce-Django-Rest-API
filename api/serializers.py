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
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        depth=1
        fields = ('order','product_id','order_quantity','order_date','order_status')


class SaleSerializer(serializers.ModelSerializer):
    order_status = ChoiceField(choices=Sale.SALE_STATUS)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Sale
        fields = ('order_id','delivery_id','delivery_date', 'confirm_date','reference','order_status')
