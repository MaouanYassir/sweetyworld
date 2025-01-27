from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date

from shop.models import Cart, CartItem, Product, Order
from django.contrib import messages


# @login_required
# def cart_view(request):
#     # Récupérer ou créer un panier pour l'utilisateur connecté
#     cart_user, created = Cart.objects.get_or_create(user=request.user)
#
#     # Récupérer tous les articles du panier de l'utilisateur
#     cart_items = CartItem.objects.filter(cart=cart_user)
#
#     # Vérifier si le panier contient des articles
#     if not cart_items.exists():
#         total_price = 0
#     else:
#         # Calculer le prix total du panier
#         total_price = sum(item.product.price * item.quantity for item in cart_items)
#
#     # calculer le total par article
#     for item in cart_items:
#         item.total_price_item = item.product.price * item.quantity
#
#     # Rendre le template avec les données du panier
#     return render(request, "shop/cart.html", context={
#         "cart_user": cart_user,
#         "cart_items": cart_items,
#         "total_price": total_price,
#
#     })


@login_required
def cart_view(request):
    # Récupérer ou créer un panier pour l'utilisateur connecté
    cart_user, created = Cart.objects.get_or_create(user=request.user)

    # Récupérer tous les articles du panier de l'utilisateur
    cart_items = CartItem.objects.filter(cart=cart_user)

    # Calculer le prix total du panier
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # calculer le total par article
    for item in cart_items:
        item.total_price_item = item.product.price * item.quantity

    # Si la requête est une soumission POST (pour la date de retrait)
    if request.method == 'POST':
        pick_up_date_str = request.POST.get('pick_up_date')  # Récupérer la date de retrait depuis POST
        if pick_up_date_str:
            pick_up_date = parse_date(pick_up_date_str)  # Convertir la chaîne en objet date

            if not pick_up_date:
                messages.error(request, "Date de retrait invalide. Veuillez choisir une date correcte.")
                return redirect('cart_view')

            # Enregistrer la date de retrait dans le panier
            cart_user.pick_up_date = pick_up_date
            cart_user.save()

            # Vérification du quota des 30 gâteaux pour cette date
            orders_on_date = Order.objects.filter(pick_up_date=pick_up_date)
            total_quantity = sum(sum(item.quantity for item in order.order_items.all()) for order in orders_on_date)

            # Ajouter les articles du panier de l'utilisateur en cours au total
            total_quantity += sum(item.quantity for item in cart_items)

            if total_quantity >= 30:
                messages.error(request,
                               f"Le quota des 30 gâteaux a été atteint pour la date {pick_up_date}. Veuillez choisir une autre date.")
                return redirect('cart_view')

            # Si le quota n'est pas atteint, afficher un message de succès
            messages.success(request,
                             f"Date de retrait {pick_up_date} confirmée. Vous pouvez maintenant procéder au paiement.")
            return redirect('create_checkout_session', order_id=cart_user.id)  # Redirection vers Stripe

    # Rendre le template avec les données du panier
    return render(request, "shop/cart.html", context={
        "cart_user": cart_user,
        "cart_items": cart_items,
        "total_price": total_price,
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
        # messages.success(request, "Article ajouté au panier")
        cart_item.save()

    # Afficher le contenu du panier pour le débogage
    cart_items = CartItem.objects.filter(cart=cart_user)
    print(f"Articles dans le panier après ajout : {[item.product.name for item in cart_items]}")

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


# Fonction pour créer l'ordre après un paiement réussi
def create_order(request, cart_id):
    # Récupérer le panier
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    # Créer une commande avec les articles du panier
    order = Order.objects.create(
        user=request.user,
        cart=cart,  # Associe la commande avec le panier
        total_price=cart.total_price,  # Assure-toi d'ajouter le prix total de la commande
        pick_up_date=cart.pick_up_date,  # Si tu utilises cette date
    )

    # Associer les items du panier à la commande
    for item in cart.cartitem_set.all():
        CartItem.objects.create(
            order=order,  # Associer l'item à la commande
            product=item.product,
            quantity=item.quantity,
        )

    # Vider le panier après la création de la commande
    cart.cartitem_set.all().delete()

    # Marquer la commande comme payée
    order.is_paid = True
    order.save()

    # Retourner ou rediriger après la création
    return redirect('index_view')
