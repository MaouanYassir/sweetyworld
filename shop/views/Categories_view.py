from django.shortcuts import render

from shop.models import Category


def categories_view(request):
    categories = Category.objects.all()
    return render(request, "shop/categories.html", {'categories': categories})