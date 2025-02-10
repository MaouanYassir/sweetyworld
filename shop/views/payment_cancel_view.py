from django.shortcuts import redirect
from django.contrib import messages


def payment_cancel(request, cart_id):
    # Afficher un message d'erreur ou d'annulation
    messages.warning(request, "Le paiement a été annulé. Votre panier est toujours disponible.")

    # Rediriger vers le panier
    return redirect('cart_view')