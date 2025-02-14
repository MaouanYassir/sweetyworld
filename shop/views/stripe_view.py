

import stripe
from django.shortcuts import get_object_or_404, redirect
from config import settings
from shop.models import Cart, CartItem

# Configurer Stripe avec la clé secrète
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, cart_id):
    # Récupérer le panier pour l'utilisateur connecté
    cart_user = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_user)

    # Calculer le prix total du panier
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Créer la session de paiement Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f"Panier de {cart_user.user.email}",
                },
                'unit_amount': int(total_price * 100),  # Prix total en centimes
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/order/success/{cart_id}/'),  # Assure-toi que cette URL est correcte
        cancel_url=request.build_absolute_uri(f'/order/cancel/{cart_id}/'),
    )

    # Rediriger vers la page de paiement Stripe
    return redirect(session.url, code=303)


