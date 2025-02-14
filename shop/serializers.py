from rest_framework import serializers
from .models import CartItem, Order


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    total_price_item = serializers.DecimalField( max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['product_name', 'quantity', 'product_price', 'total_price_item']


class OrderSerializer(serializers.ModelSerializer):
    order_items = CartItemSerializer(many=True)
    user_email = serializers.CharField(source='user.email')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_email', 'order_date', 'is_paid', 'pick_up_date', 'total_price', 'order_items']
