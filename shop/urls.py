from django.urls import path, include
from rest_framework.permissions import IsAdminUser
from rest_framework.routers import DefaultRouter
from shop.views.API_view import OrderListView, ProductViewSet, OrderDetailView
from shop.views.CGV_view import CGV_view
from shop.views.cookie_view import cookies_policy
from shop.views.cookies_settings_view import cookies_settings_view
from shop.views.generate_invoice_view import generate_invoice
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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# vue de documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API SweetyWorld",
        default_version='v1',
        description="Document détaillant les endpoints de l'API",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[IsAdminUser],
)

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
    path('invoice/<int:order_id>/', generate_invoice, name='generate_invoice'),
    path('CGV/', CGV_view, name='CGV_view'),
    path('cookies/', cookies_policy, name='cookies_policy'),
    path('cookies_settings/', cookies_settings_view, name='cookies_settings'),

    # api des commandes http://127.0.0.1:8000/api/orders/
    path('api/orders/', OrderListView.as_view(), name='order_list'),

    # L'endpoint pour obtenir une commande spécifique par son ID http://127.0.0.1:8000/api/orders/1/
    path('api/orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),


    # API des produits (get = liste ou produit spécifique, post= ajouter un produits , delete= supprimer un produit, put= modifier un produit
    # http://127.0.0.1:8000/api/products/ pour afficher la liste de produits (get), et en créer un nouveau (post)
    # http://127.0.0.1:8000/api/products/6/ pour afficher un produit spécifique de par son id et pouvoir le  modifier(put) ou le supprimer(delete)
    path('api/', include(router.urls)),  # Toutes les URL générées par le router pour les produits


    # tester avec: http://127.0.0.1:8000/swagger/
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),  # URL de la documentation Swagger

]

