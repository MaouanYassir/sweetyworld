# from django.shortcuts import redirect
# from django.contrib import messages
#
#
# def payment_cancel(request, cart_id):
#     # Afficher un message d'erreur ou d'annulation
#     messages.warning(request, "Le paiement a été annulé. Votre panier est toujours disponible.")
#
#     # Rediriger vers le panier
#     return redirect('cart_view')

from django.shortcuts import get_object_or_404, render

from shop.models import Order


def payment_cancel(request, order_id):
    # récupere la commande
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "shop/payment_cancel.html", {'order': order})