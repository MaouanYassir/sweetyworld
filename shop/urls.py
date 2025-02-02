from django.urls import path

from .views import payment_success, payment_cancel, user_orders_view
from .views.cart_view import cart_view, add_to_cart_view, remove_from_cart_view, clear_cart_view, create_order
from .views.category_view import category_view
from .views.Categories_view import categories_view
from .views.index_view import index_view
from .views.stripe_view import create_checkout_session

urlpatterns = [
    path('', index_view, name='index_view'),
    path('categories/', categories_view, name='categories_view'),
    path('category/<slug:slug>/', category_view, name='category_view'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/create-order/', create_order, name='create-order'),
    path('add_to_cart/<slug:slug>/', add_to_cart_view, name='add_to_cart_view'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart_view, name='remove_from_cart_view'),
    path('clear_cart/', clear_cart_view, name='clear_cart_view'),
    path('create_checkout_session/<int:order_id>/', create_checkout_session, name='create_checkout_session'),
    path('order/success/<int:order_id>/', payment_success, name='payment_success'),
    path('order/cancel/<int:order_id>/', payment_cancel, name='payment_cancel'),
    path('user_orders/', user_orders_view, name='user_orders_view'),
]


