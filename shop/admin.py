from django.contrib import admin
from django.utils.html import format_html
from .models.contactMessage import ContactMessage
from shop.models import Product, Category, CartItem, Order


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)
    list_display_links = ('name',)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('categories',)
    list_display = ('name', 'categories', 'price',)
    list_display_links = ('name',)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent', 'reply_link')

    def reply_link(self, obj):
        # Crée un lien pour ouvrir Outlook avec les informations du message
        mailto_link = f"mailto:{obj.email}?subject=Réponse à votre message : {obj.subject}&body="
        return format_html(f'<a href="{mailto_link}" target="_blank">Répondre</a>')

    reply_link.short_description = "Répondre"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')  # Les champs du produit et de la quantité sont en lecture seule


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid' , "pick_up_date", 'total_price', 'get_cart_items')
    list_filter = ['is_paid', "pick_up_date"]
    actions = ["mark_as_paid"]
    inlines = [CartItemInline]  # Inline pour afficher le panier associé à la commande

    def get_cart_items(self, obj):
        """Récupère les produits associés à la commande."""
        cart_items = obj.order_items.all()  # Utilise 'order_items' pour accéder aux articles associés à la commande
        if cart_items.exists():  # Vérifie si des articles sont associés
            items = ", ".join([f"{item.product.name} (x{item.quantity})" for item in cart_items])
            return items
        else:
            return "Aucun article"  # Retourne ce message si aucun article n'est trouvé

    get_cart_items.short_description = "Articles dans la commande"  # Titre de la colonne


admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
