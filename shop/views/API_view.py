from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser  # Permet l'accès uniquement à l'admin
from shop.models import Order, Product
from shop.serializers import OrderSerializer, ProductSerializer


# ----------------------------------vue pour les commandes--------------------------------------------------------------
class OrderListView(APIView):
    permission_classes = [IsAdminUser]  # Seul l'administrateur peut accéder à cette vue

    def get(self, request):
        # Récupérer toutes les commandes
        orders = Order.objects.all()  # Récupère toutes les commandes
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ---------------------------------------vue pour les produits----------------------------------------------------------

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Récupère tous les produits
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]  # Limite l'accès à l'admin uniquement