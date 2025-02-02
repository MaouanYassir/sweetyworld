import stripe
from django.shortcuts import get_object_or_404, redirect

from config import settings
from shop.models import Cart, CartItem

# # Configurer Stripe avec la clé secrète
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# def create_checkout_session(request, cart_id):
#     # Récupérer le panier de l'utilisateur
#     cart = get_object_or_404(Cart, id=cart_id, user=request.user)
#
#     # Créer la session de paiement Stripe
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price_data': {
#                 'currency': 'eur',
#                 'product_data': {
#                     'name': f"Panier de {cart.user.email}",
#                 },
#                 'unit_amount': int(sum(item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart)) * 100),  # Le prix total du panier en centimes
#             },
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=request.build_absolute_uri(f'/payment_success/{cart_id}/'),
#         cancel_url=request.build_absolute_uri(f'/payment_cancel/{cart_id}/'),
#     )
#
#     # Redirection vers Stripe Checkout pour paiement
#     return redirect(session.url, code=303)

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from shop.models import Order

# Configurer Stripe avec la clé secrète
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, order_id):
    # Récupérer la commande pour l'utilisateur connecté
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Créer une session de paiement Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f"Commande n°{order.id}",
                },
                'unit_amount': int(order.total_price * 100),  # Stripe travaille en centimes
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/order/success/{order.id}/'),
        cancel_url=request.build_absolute_uri(f'/order/cancel/{order.id}/'),
    )

    return redirect(session.url, code=303)
