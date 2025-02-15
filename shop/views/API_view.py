from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser  # Permet l'accès uniquement à l'admin
from shop.models import Order, Product
from shop.serializers import OrderSerializer, ProductSerializer
from rest_framework.generics import get_object_or_404


# ----------------------------------vue pour la liste des commandes--------------------------------------------------------------
class OrderListView(APIView):
    permission_classes = [IsAdminUser]  # Seul l'administrateur peut accéder à cette vue

    def get(self, request):
        # Récupérer toutes les commandes
        orders = Order.objects.all()  # Récupère toutes les commandes
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------------------------vue pour une commande spécifique------------------------------------------------
class OrderDetailView(APIView):
    permission_classes = [IsAdminUser]  # Seul l'administrateur peut accéder à cette vue

    def get(self, request, order_id):
        # Récupérer la commande par son ID, avec une gestion d'erreur si la commande n'existe pas
        order = get_object_or_404(Order, id=order_id)

        # Sérialiser la commande
        serializer = OrderSerializer(order)

        # Retourner la réponse avec les données de la commande
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------------vue pour les produits----------------------------------------------------------

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Récupère tous les produits
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]  # Limite l'accès à l'admin uniquement
