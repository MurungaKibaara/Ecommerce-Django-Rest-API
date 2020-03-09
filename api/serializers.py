from rest_framework import serializers
from .models import Product, Order, Sale, Category

class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id','category', 'product_name', 'product_description', 'product_quantity', 'product_price', 'created','featured','updated')

class OrderSerializer(serializers.ModelSerializer):
    order_status = ChoiceField(choices=Order.STATUS)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ('order','product_id','order_quantity','created','order_status', 'updated')

class SaleSerializer(serializers.ModelSerializer):
    order_status = ChoiceField(choices=Sale.SALE_STATUS)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Sale
        fields = ('order_id','delivery_id','delivery_date', 'confirm_date','reference','order_status', 'updated')
