from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from shop.models import Cart, CartItem, Product
from django.contrib import messages


@login_required
def cart_view(request):
    # Récupérer ou créer un panier pour l'utilisateur connecté
    cart_user, created = Cart.objects.get_or_create(user=request.user)

    # Récupérer tous les articles du panier de l'utilisateur
    cart_items = CartItem.objects.filter(cart=cart_user)

    # Vérifier si le panier contient des articles
    if not cart_items.exists():
        messages.warning(request, "Votre panier est vide.")
        total_price = 0
    else:
        # Calculer le prix total du panier
        total_price = sum(item.product.price * item.quantity for item in cart_items)

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
