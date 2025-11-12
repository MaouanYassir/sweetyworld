from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from shop.models import Product, CartItem
from django.db.models import Q




def index_view(request):
    # Date actuelle
    now = timezone.now()

    # Annotation des ventes : 6 mois, futures, et totales (passées + futures)
    products = Product.objects.annotate(
        # --- Ventes des 6 derniers mois ---
        total_sales_last_6_months=Coalesce(Sum(
            'cartitem__quantity',
            filter=Q(
                cartitem__order__order_date__gte=now - timezone.timedelta(days=180),
                cartitem__order__order_date__lte=now,
                cartitem__order__pick_up_date__lte=now  # exclure les futures
            )
        ), Value(0)),

        # --- Ventes futures ---
        total_sales_future=Coalesce(Sum(
            'cartitem__quantity',
            filter=Q(cartitem__order__pick_up_date__gte=now)
        ), Value(0)),

        # --- Ventes totales (passées + futures) ---
        total_sales_all_time=Coalesce(Sum(
            'cartitem__quantity',
            filter=Q(cartitem__order__pick_up_date__isnull=False)
        ), Value(0))
    ).annotate(
        # --- Combinaison : pour garder la logique “bestsellers” cohérente
        total_sales_combined=F('total_sales_all_time')
    ).order_by('-total_sales_combined')[:3]  # ← affiche les 3 produits les plus vendus

    # Envoi au template
    return render(request, 'shop/index.html', {'products': products})