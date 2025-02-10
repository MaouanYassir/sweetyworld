
from django.shortcuts import get_object_or_404, redirect
from shop.models import Cart, CartItem, Order


def create_order(request, cart_id):
    cart_user = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_user)

    # Calculer le prix total du panier
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Créer la commande
    order = Order.objects.create(
        cart=cart_user,
        user=request.user,
        pick_up_date=cart_user.pick_up_date,  # Tu peux récupérer la date de retrait depuis le panier si nécessaire
        total_price=total_price,
        is_paid=True  # Mettre l'état du paiement à True
    )

    for item in cart_items:
        # Créer une nouvelle instance de CartItem associée à la commande
        CartItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            cart=cart_user
        )

    # Vider le panier après le paiement
    cart_user.delete()

    # return redirect('payment_success', cart_id=cart_user.id)
    return redirect('payment_success_confirmation', order_id=order.id)
