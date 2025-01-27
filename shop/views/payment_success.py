from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from shop.models import Order, Cart, CartItem
from .cart_view import create_order


def payment_success(request, cart_id):
    # Récupérer le panier
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)



    # Afficher un message de succès
    messages.success(request, "Paiement réussi et commande créée ! Votre panier a été vidé.")

    # Rediriger vers la page de confirmation
    return redirect('payment_success')