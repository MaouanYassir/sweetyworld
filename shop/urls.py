from django.urls import path

from .views.cart_view import cart_view, add_to_cart_view, remove_from_cart_view, clear_cart_view
from .views.category_view import category_view
from .views.Categories_view import categories_view
from .views.index_view import index_view

urlpatterns = [
    path('', index_view, name='index_view'),
    path('categories/', categories_view, name='categories_view'),
    path('category/<slug:slug>/', category_view, name='category_view'),
    path('cart/', cart_view, name='cart_view'),
    path('add_to_cart/<slug:slug>/', add_to_cart_view, name='add_to_cart_view'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart_view, name='remove_from_cart_view'),
    path('clear_cart/', clear_cart_view, name='clear_cart_view'),
]