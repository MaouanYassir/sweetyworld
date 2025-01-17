from django.shortcuts import get_object_or_404, render

from ..models import Category, Product


def category_view(request, slug):
    # Récupérer la catégorie par son slug
    category = get_object_or_404(Category, slug=slug)
    # Filtrer les produits associés à cette catégorie
    products = Product.objects.filter(category=category)

    # Passer l'objet category et les produits au template
    return render(request, 'shop/category.html', {'products': products,
                                                  'category': category})
