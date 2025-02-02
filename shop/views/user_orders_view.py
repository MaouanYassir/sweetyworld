from django.shortcuts import render

from shop.models import Order


def user_orders_view(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, "shop/user_orders.html", {'orders': orders})
