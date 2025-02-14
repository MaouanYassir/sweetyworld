from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views.API_view import OrderListView, ProductViewSet
from shop.views.payment_cancel_view import payment_cancel
from shop.views.payment_success_confirmation_view import payment_success_confirmation
from shop.views.create_order_view import create_order
from shop.views.stripe_view import create_checkout_session
from shop.views.user_orders_view import user_orders_view
from shop.views.about_view import about_view
from shop.views.cart_view import cart_view, add_to_cart_view, remove_from_cart_view, clear_cart_view, check_quota
from shop.views.categories_view import categories_view
from shop.views.category_view import category_view
from shop.views.contact_view import contact_view
from shop.views.shop_view import index_view

# Créer un router et enregistrer le ProductViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')  # Route pour les produits

urlpatterns = [
    path('', index_view, name='home'),
    path('categories/', categories_view, name='categories_view'),
    path('categories/<slug:slug>/', category_view, name='category_view'),
    path('about/', about_view, name='about_view'),
    path('contact/', contact_view, name='contact_view'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/check_quota/', check_quota, name='check_quota'),
    path('add_to_cart/<slug:slug>/', add_to_cart_view, name='add_to_cart_view'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart_view, name='remove_from_cart_view'),
    path('clear_cart/', clear_cart_view, name='clear_cart_view'),
    path('user_orders/', user_orders_view, name='user_orders_view'),
    path('create-checkout-session/<int:cart_id>/', create_checkout_session, name='create_checkout_session'),
    path('order/success/<int:cart_id>/', create_order, name='create_order'),
    path('order/success/confirmation/<int:order_id>/', payment_success_confirmation, name='payment_success_confirmation'),
    path('order/cancel/<int:cart_id>/', payment_cancel, name='payment_cancel'),

    # api des commandes
    path('api/orders/', OrderListView.as_view(), name='order_list'),

    # API des produits (get = liste ou produit spécifique, post= ajouter un produits , delete= supprimer un produit, put= modifier un produit
    # http://127.0.0.1:8000/api/products/ pour afficher la liste de produits (get), et en créer un nouveau (post)
    # http://127.0.0.1:8000/api/products/6/ pour afficher un produit spécifique de par son id et pouvoir le  modifier(put) ou le supprimer(delete)
    path('api/', include(router.urls)),  # Toutes les URL générées par le router pour les produits
]
