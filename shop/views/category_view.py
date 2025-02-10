from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product



def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(categories=category)
    return render(request, 'shop/category.html', {'products': products,
                                                  'category_name': category.name})
