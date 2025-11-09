from django.db.models import Sum
from .models.cart_model import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_quantity = (
            CartItem.objects.filter(cart=cart)
            .aggregate(total=Sum("quantity"))["total"]
            or 0
        )
    else:
        total_quantity = 0
    return {'cart_item_count': total_quantity}
