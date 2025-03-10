from django.shortcuts import render

from shop.models import Category


def categories_view(request):
    categories = Category.objects.all()
    from django.utils.translation import get_language
    language = get_language()  # Obtient la langue courante
    return render(request, 'shop/categories.html', {'categories': categories, 'language': language})
