# tout les models concernant le panier sont ici
from django.db import models
from django.core.exceptions import ValidationError
from config import settings
from shop.models import Product


# from . import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    pick_up_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"panier de {self.user.email if self.user else 'utilisateur inconnu'}"


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    pick_up_date = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"commande de {self.user.email} | date de la commande {self.order_date} | date de retrait{self.pick_up_date}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='order_items')  # Lien avec Order

    @property
    def total_price_item(self):
        # Calcul du prix total pour un article dans le panier
        # Le prix total de l'article est calculé en multipliant le prix du produit par la quantité
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        # Cette méthode `save` est appelée avant de sauvegarder un objet CartItem dans la base de données

        if not self.cart:
            # Si l'objet CartItem n'est pas associé à un panier (cart), une erreur de validation est levée
            raise ValidationError("Un CartItem doit être associé à un Cart.")

        # Appel de la méthode `save` de la classe parente pour sauvegarder l'objet dans la base de données
        super().save(*args, **kwargs)

    def __str__(self):
        if self.cart and self.cart.user:
            return f"{self.quantity} {self.product.name} dans le panier de {self.cart.user.email}"
        return f"{self.quantity} {self.product.name} dans un panier sans utilisateur"