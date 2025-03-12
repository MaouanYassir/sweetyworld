from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from shop.models import Product, CartItem
from django.db.models import Q


def index_view(request):
    # Calcul des ventes combinées : ventes des 6 derniers mois + ventes futures
    products = Product.objects.annotate(
        # Annotation de la vente des 6 derniers mois pour chaque produit
        total_sales_last_6_months=Sum(
            'cartitem__quantity',  # Somme des quantités d'articles dans les CartItems
            filter=Q(cartitem__order__order_date__gte=timezone.now() - timezone.timedelta(days=180),  # Date de commande dans les 6 derniers mois
                     cartitem__order__order_date__lte=timezone.now(),  # Jusqu'à aujourd'hui
                     cartitem__order__pick_up_date__lte=timezone.now())  # Date de retrait passée (exclure les commandes futures)
        ),
        # Annotation des ventes futures (quantités d'articles qui ont une date de retrait future)
        total_sales_future=Sum(
            'cartitem__quantity',  # Somme des quantités d'articles dans les CartItems
            filter=Q(cartitem__order__pick_up_date__gte=timezone.now())  # Date de retrait future
        )
    ).annotate(
        # Remplacer les valeurs None par 0 pour les ventes des 6 derniers mois
        total_sales_last_6_months=Coalesce('total_sales_last_6_months', Value(0)),
        # Remplacer les valeurs None par 0 pour les ventes futures
        total_sales_future=Coalesce('total_sales_future', Value(0)),
        # Calcul des ventes combinées en additionnant les ventes des 6 derniers mois et les ventes futures
        total_sales_combined=F('total_sales_last_6_months') + F('total_sales_future')
    ).order_by('-total_sales_combined')[:3]  # Trier par les meilleures ventes (en fonction des ventes combinées) et afficher les 3 meilleurs produits

    # Passer les produits annotés (avec les données des ventes combinées) au template pour affichage
    return render(request, 'shop/index.html', {'products': products})

