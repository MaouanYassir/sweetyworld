from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from shop.models import Product
from shop.models.cart_model import Cart, CartItem, Order
from django.utils.translation import get_language
from django.utils.timezone import make_aware


@login_required
def cart_view(request):
    # Récupérer ou créer un panier pour l'utilisateur connecté
    cart_user, created = Cart.objects.get_or_create(user=request.user)

    # Récupérer tous les articles du panier de l'utilisateur
    cart_items = CartItem.objects.filter(cart=cart_user)

    # Vérifier si le panier contient des articles
    if not cart_items.exists():
        total_price = 0
    else:
        # Calculer le prix total du panier
        total_price = sum(item.product.price * item.quantity for item in cart_items)


    # Rendre le template avec les données du panier
    return render(request, "shop/cart.html", context={
        "cart_user": cart_user,
        "cart_items": cart_items,
        "total_price": total_price,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,  # Clé publique passée au template

    })

# fonction check_quota SANS le quota des 30 gateaux quotidien
# @login_required
# def check_quota(request):
#     # Récupérer le panier pour l'utilisateur connecté
#     cart_user = get_object_or_404(Cart, user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart_user)
#
#     # Calculer la date minimale autorisée (3 jours plus tard)
#     min_pick_up_date = make_aware(datetime.now() + timedelta(days=3))
#     min_pick_up_date = min_pick_up_date.replace(hour=0, minute=0, second=0, microsecond=0)
#
#     # Détecter la langue de l'utilisateur
#     language = get_language()
#
#     # Vérifier si la méthode de la requête est POST
#     if request.method == "POST":
#         # Récupérer la date de retrait choisie
#         pick_up_date_str = request.POST.get('pick_up_date')
#
#         try:
#             pick_up_date = make_aware(datetime.fromisoformat(pick_up_date_str))
#         except ValueError:
#             messages.error(request, "Date invalide.")
#             return redirect('cart_view')
#
#         # Sauvegarder la date dans le panier
#         cart_user.pick_up_date = pick_up_date
#         cart_user.save()
#
#         # Vérifier si la date est valide (au moins 3 jours plus tard)
#         if pick_up_date >= min_pick_up_date:
#             return redirect('create_checkout_session', cart_id=cart_user.id)
#         else:
#             message = (
#                 f"Veuillez choisir une date à partir du {min_pick_up_date.strftime('%d/%m/%Y')}."
#                 if language == 'fr' else
#                 f"Kies een datum vanaf {min_pick_up_date.strftime('%d/%m/%Y')}."
#             )
#             messages.error(request, message)
#
#     return render(request, "shop/cart.html", {
#         "cart_user": cart_user,
#         "cart_items": cart_items,
#         "min_pick_up_date": min_pick_up_date,
#     })


# fonction check_quota AVEC le quota des 30 gateaux quotidien
@login_required
def check_quota(request):   # fonction qui contrôle le quota sans créer l'order
    # Récupérer le panier pour l'utilisateur connecté
    cart_user = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_user)

    # Calculer la date minimale autorisée (3 jours plus tard)
    min_pick_up_date = make_aware(datetime.now() + timedelta(days=3))
    min_pick_up_date = min_pick_up_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # Détecter la langue de l'utilisateur
    language = get_language()

    # Vérifier si la méthode de la requête est POST (soumission du formulaire pour date de retrait)
    if request.method == "POST":
        # Récupérer la date de retrait saisie par l'utilisateur dans le formulaire
        pick_up_date_str = request.POST.get('pick_up_date')

        # Convertir la chaîne de caractères de la date en objet datetime
        pick_up_date = make_aware(datetime.fromisoformat(pick_up_date_str))
        cart_user.pick_up_date = pick_up_date  # Ajouter la date de retrait au panier
        cart_user.save()  # Sauvegarder la date dans le panier

        # Vérifier si la date choisie est au moins 3 jours plus tard
        if pick_up_date >= min_pick_up_date:
            # Vérifier si des commandes existent déjà pour cette date
            orders_on_date = Order.objects.filter(pick_up_date=pick_up_date)
            total_quantity_existing_orders = sum(
                sum(item.quantity for item in order.order_items.all()) for order in orders_on_date
            )

            # Ajouter la quantité des articles de la commande en cours au total
            total_quantity_with_current_order = total_quantity_existing_orders + sum(
                item.quantity for item in cart_items)

            # Cas 1 : Si des commandes existent déjà et que le quota de 30 gâteaux est dépassé
            if total_quantity_with_current_order > 30:
                remaining_quantity = 30 - total_quantity_existing_orders
                if remaining_quantity > 0:
                    message = (
                        f"Nous acceptons un maximum de 30 gâteaux par jour. Pour la date choisie, vous pouvez encore commander maximum {remaining_quantity} gâteau(x)."
                        if language == 'fr' else
                        f"We accepteren maximaal 30 taarten per dag. Voor de gekozen datum kunt u nog {remaining_quantity} taart(en) maximum bestellen."
                    )
                else:
                    message = (
                        "Le quota de 30 gâteaux pour cette date est déjà atteint. Vous ne pouvez pas commander plus de gâteaux."
                        if language == 'fr' else
                        "Het quotum van 30 taarten voor deze datum is al bereikt. U kunt geen extra taarten bestellen."
                    )
                messages.error(request, message)

            # Cas 2 : Si aucune commande n'a été passée pour cette date et que le client tente de commander plus de 30 gâteaux
            elif total_quantity_existing_orders == 0 and total_quantity_with_current_order > 30:
                message = (
                    "Le quota maximum de 30 gâteaux par jour est atteint. Vous ne pouvez pas commander plus de 30 gâteaux."
                    if language == 'fr' else
                    "Het maximale quotum van 30 taarten per dag is bereikt. U kunt niet meer dan 30 taarten bestellen."
                )
                messages.error(request, message)

            # Si la commande n'excède pas le quota de 30 gâteaux
            else:
                # Créer une session de paiement avec Stripe
                return redirect('create_checkout_session', cart_id=cart_user.id)  # Rediriger vers Stripe pour payer

        else:
            # Si la date est dans le passé ou avant 3 jours, ajouter un message d'erreur
            message = (
                f"Veuillez choisir une date à partir du {min_pick_up_date.strftime('%d/%m/%Y')}."
                if language == 'fr' else
                f"Kies een datum vanaf {min_pick_up_date.strftime('%d/%m/%Y')}."
            )
            messages.error(request, message)

    return render(request, "shop/cart.html", {
        "cart_user": cart_user,
        "cart_items": cart_items,
        "min_pick_up_date": min_pick_up_date,
    })




def add_to_cart_view(request, slug):
    # Récupérer ou créer un panier pour l'utilisateur connecté
    cart_user, cart_user_created = Cart.objects.get_or_create(user=request.user)
    # Récupérer le produit basé sur le slug
    product = get_object_or_404(Product, slug=slug)
    # Récupérer ou créer l'élément du panier pour ce produit
    cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart_user, product=product)

    # Si l'élément existe déjà, incrémenter la quantité
    if not cart_item_created:  # Si l'élément n'est pas nouvellement créé
        cart_item.quantity += 1
        cart_item.save()

        # Afficher le contenu du panier pour le débogage
        cart_items = CartItem.objects.filter(cart=cart_user)

    # Vérifier si la requête est une requête AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Retourner une réponse JSON si la requête est faite avec AJAX
        return JsonResponse({'success': True, 'cart_item_count': cart_item.quantity})
    else:
        # Redirection classique si ce n'est pas une requête AJAX
        return redirect("cart_view")


def remove_from_cart_view(request, slug):
    # Récupérer le panier de l'utilisateur connecté
    cart_user = get_object_or_404(Cart, user=request.user)

    # Récupérer le produit en fonction du slug
    product = get_object_or_404(Product, slug=slug)

    # Obtenir l'élément de panier pour le produit spécifié
    cart_item = get_object_or_404(CartItem, cart=cart_user, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart_view")


def clear_cart_view(request):
    cart_user = get_object_or_404(Cart, user=request.user)

    cart_user.cartitem_set.all().delete()

    return redirect("cart_view")
