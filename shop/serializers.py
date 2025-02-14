from rest_framework import serializers
from .models import CartItem, Order, Product


# ----------------------------- serializer pour OrderListView--------------------------------------------------------
class CartItemSerializer(serializers.ModelSerializer):
    # Récupère le nom du produit associé à ce CartItem
    product_name = serializers.CharField(source='product.name')

    # Récupère le prix du produit associé à ce CartItem
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)

    # Calcule le prix total de l'article dans le panier (quantité * prix)
    total_price_item = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Spécifie le modèle que ce sérialiseur va transformer en JSON
        model = CartItem
        # Les champs que nous voulons exposer dans la réponse JSON
        fields = ['product_name', 'quantity', 'product_price', 'total_price_item']


class OrderSerializer(serializers.ModelSerializer):
    # Utilisation du sérialiseur CartItemSerializer pour inclure tous les articles de la commande
    order_items = CartItemSerializer(many=True)

    # Récupère l'email de l'utilisateur associé à cette commande
    user_email = serializers.CharField(source='user.email')

    # Le prix total de la commande, qui est déjà calculé dans le modèle et marqué comme "read_only"
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        # Spécifie le modèle que ce sérialiseur va transformer en JSON
        model = Order
        # Les champs que nous voulons exposer dans la réponse JSON
        fields = ['id', 'user_email', 'order_date', 'is_paid', 'pick_up_date', 'total_price', 'order_items']


# --------------------------------------serializer pour ProductViewSet-------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Les champs à exposer pour un produit
        fields = ['id', 'name', 'description', 'slug', 'image', 'price', 'categories', 'created_date', 'modified_date']
