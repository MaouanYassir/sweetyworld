from django.db.models import Sum
from django.shortcuts import render

from shop.models import Product


def index_view(request):
    # Récupérer les produits triés par le total des ventes, en affichant les 3 produits les plus vendus
    products = Product.objects.annotate(total_sales=Sum('cartitem__quantity')).order_by('-total_sales')[:3]

    # Passer les produits au template
    return render(request, 'shop/index.html', {'products':products})