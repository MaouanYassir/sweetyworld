# from django.contrib import messages
# from django.shortcuts import get_object_or_404, redirect, render
# from shop.models import Order, Cart, CartItem
# from .cart_view import create_order
#
#
# def payment_success(request, cart_id):
#     # Récupérer le panier à partir du cart_id
#     cart = get_object_or_404(Cart, id=cart_id, user=request.user)
#
#     total_price = sum(item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart))
#
#
#     # Passer la variable 'cart' au template pour afficher des informations supplémentaires
#     return render(request, 'shop/payment_success.html', {'cart': cart, 'total_price': total_price})


from django.shortcuts import get_object_or_404, render

from shop.models import Order


def payment_success(request, order_id):
    # recupere la commande
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # marquer la commande comme payée
    order.is_paid = True
    order.save()

    return render(request, "shop/payment_success.html", {'order': order})
