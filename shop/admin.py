#
#
# from django.contrib import admin
# from django.utils import timezone
# from django.db.models import Sum, Q
# from django.utils.html import format_html
# from .models.contactMessage import ContactMessage
# from shop.models import Product, Category, CartItem, Order
#
#
# # Filtre personnalisé pour la période de vente
# class SalesPeriodFilter(admin.SimpleListFilter):
#     title = 'Période de vente'
#     parameter_name = 'sales_period'
#
#     def lookups(self, request, model_admin):
#         return [
#             ('last_month', 'Dernier mois'),
#             ('last_6_months', '6 derniers mois'),
#             ('future', 'Période future')
#         ]
#
#     def queryset(self, request, queryset):
#         now = timezone.now()
#
#         if self.value() == 'last_month':
#             # Filtrer pour le dernier mois
#             start_date = now - timezone.timedelta(days=30)
#             return queryset.filter(order__order_date__gte=start_date)
#
#         if self.value() == 'last_6_months':
#             # Filtrer pour les six derniers mois
#             start_date = now - timezone.timedelta(days=180)
#             return queryset.filter(order__order_date__gte=start_date)
#
#         if self.value() == 'future':
#             # Filtrer pour les commandes futures
#             return queryset.filter(order__pick_up_date__gte=now)
#
#         return queryset
#
#
# # ModelAdmin pour la catégorie
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ('name',)
#     list_display_links = ('name',)
#
#
# # ModelAdmin pour le produit
# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_filter = ('categories', SalesPeriodFilter)  # Appliquer le filtre personnalisé pour la période
#     list_display = (
#     'name', 'categories', 'price', 'total_sales_last_month', 'total_sales_last_6_months', 'total_sales_future')
#     list_display_links = ('name',)
#
#     def total_sales_last_month(self, obj):
#         # Calculer les ventes du dernier mois, en comptant la quantité vendue
#         start_date = timezone.now() - timezone.timedelta(days=30)
#         return CartItem.objects.filter(product=obj, order__order_date__gte=start_date).aggregate(
#             total_sales=Sum('quantity'))['total_sales'] or 0
#
#     def total_sales_last_6_months(self, obj):
#         # Calculer les ventes des 6 derniers mois, en comptant la quantité vendue
#         start_date = timezone.now() - timezone.timedelta(days=180)
#         return CartItem.objects.filter(product=obj, order__order_date__gte=start_date).aggregate(
#             total_sales=Sum('quantity'))['total_sales'] or 0
#
#     def total_sales_future(self, obj):
#         # Calculer les ventes futures, en comptant la quantité vendue
#         now = timezone.now()
#         return \
#             CartItem.objects.filter(product=obj, order__pick_up_date__gte=now).aggregate(total_sales=Sum('quantity'))[
#                 'total_sales'] or 0
#
#     total_sales_last_month.short_description = "Ventes du dernier mois"
#     total_sales_last_6_months.short_description = "Ventes des 6 derniers mois"
#     total_sales_future.short_description = "Ventes futures"
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#
#         # Annoter le queryset avec les données de ventes, en sommant les quantités pour chaque produit
#         queryset = queryset.annotate(
#             last_month_sales=Sum('cartitem__quantity', filter=Q(
#                 cartitem__order__order_date__gte=timezone.now() - timezone.timedelta(days=30))),
#             last_6_months_sales=Sum('cartitem__quantity', filter=Q(
#                 cartitem__order__order_date__gte=timezone.now() - timezone.timedelta(days=180))),
#             future_sales=Sum('cartitem__quantity', filter=Q(cartitem__order__pick_up_date__gte=timezone.now()))
#         ).order_by('-last_month_sales')  # Trier par les ventes du dernier mois
#
#         return queryset
#
#
# # ModelAdmin pour les messages de contact
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'date_sent', 'reply_link')
#
#     def reply_link(self, obj):
#         # Crée un lien pour ouvrir Outlook avec les informations du message
#         mailto_link = f"mailto:{obj.email}?subject=Réponse à votre message : {obj.subject}&body="
#         return format_html(f'<a href="{mailto_link}" target="_blank">Répondre</a>')
#
#     reply_link.short_description = "Répondre"
#
#
# # ModelAdmin pour CartItem
# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0
#     readonly_fields = ('product', 'quantity')  # Les champs du produit et de la quantité sont en lecture seule
#
#
# # ModelAdmin pour Order
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'is_paid', "pick_up_date", 'total_price', 'get_cart_items')
#     list_filter = ['is_paid', "pick_up_date"]
#     actions = ["mark_as_paid"]
#     inlines = [CartItemInline]  # Inline pour afficher le panier associé à la commande
#
#     def get_cart_items(self, obj):
#         """Récupère les produits associés à la commande."""
#         cart_items = obj.order_items.all()  # Utilise 'order_items' pour accéder aux articles associés à la commande
#         if cart_items.exists():  # Vérifie si des articles sont associés
#             items = ", ".join([f"{item.product.name} (x{item.quantity})" for item in cart_items])
#             return items
#         else:
#             return "Aucun article"  # Retourne ce message si aucun article n'est trouvé
#
#     get_cart_items.short_description = "Articles dans la commande"  # Titre de la colonne
#
#
# # Enregistrer les modèles dans l'admin
# admin.site.register(ContactMessage, ContactMessageAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Order, OrderAdmin)
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Q
from django.utils import timezone
from .models.contactMessage import ContactMessage
from shop.models import Product, Category, CartItem, Order


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)
    list_display_links = ('name',)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('categories',)
    list_display = (
        'name',
        'categories',
        'price',
        'total_sales_last_month',
        'total_sales_last_6_months',
        'total_sales_future',
        'total_sales_all_time',
    )
    list_display_links = ('name',)

    # --- Ventes sur 30 jours ---
    def total_sales_last_month(self, obj):
        start_date = timezone.now() - timezone.timedelta(days=30)
        return CartItem.objects.filter(
            product=obj,
            order__order_date__gte=start_date,
            order__order_date__lte=timezone.now(),
            order__pick_up_date__lte=timezone.now()
        ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0

    # --- Ventes sur 6 mois ---
    def total_sales_last_6_months(self, obj):
        start_date = timezone.now() - timezone.timedelta(days=180)
        return CartItem.objects.filter(
            product=obj,
            order__order_date__gte=start_date,
            order__order_date__lte=timezone.now(),
            order__pick_up_date__lte=timezone.now()
        ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0

    # --- Ventes futures ---
    def total_sales_future(self, obj):
        now = timezone.now()
        return CartItem.objects.filter(
            product=obj,
            order__pick_up_date__gte=now
        ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0

    # --- ✅ Ventes totales cumulées (passées + futures, sans double comptage) ---
    def total_sales_all_time(self, obj):
        now = timezone.now()
        total = CartItem.objects.filter(
            product=obj,
            order__pick_up_date__isnull=False  # on ne prend que les commandes avec une date de retrait
        ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
        return total

    total_sales_last_month.short_description = "Ventes (30 derniers jours)"
    total_sales_last_6_months.short_description = "Ventes (180 derniers jours)"
    total_sales_future.short_description = "Ventes futures"
    total_sales_all_time.short_description = "Ventes totales (passées + futures)"

    # --- Optimisation du queryset ---
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        now = timezone.now()

        queryset = queryset.annotate(
            last_month_sales=Sum(
                'cartitem__quantity',
                filter=Q(cartitem__order__order_date__gte=now - timezone.timedelta(days=30),
                         cartitem__order__order_date__lte=now,
                         cartitem__order__pick_up_date__lte=now)
            ),
            last_6_months_sales=Sum(
                'cartitem__quantity',
                filter=Q(cartitem__order__order_date__gte=now - timezone.timedelta(days=180),
                         cartitem__order__order_date__lte=now,
                         cartitem__order__pick_up_date__lte=now)
            ),
            future_sales=Sum(
                'cartitem__quantity',
                filter=Q(cartitem__order__pick_up_date__gte=now)
            ),
            all_time_sales=Sum(
                'cartitem__quantity',
                filter=Q(cartitem__order__pick_up_date__isnull=False)
            )
        ).order_by('-last_month_sales')

        return queryset


# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_filter = ('categories',)  # Appliquer un filtre pour les catégories
#     list_display = (
#         'name', 'categories', 'price', 'total_sales_last_month', 'total_sales_last_6_months', 'total_sales_future')
#     list_display_links = ('name',)
#
#     def total_sales_last_month(self, obj):
#         # Calculer les ventes du dernier mois, en comptant la quantité vendue
#         start_date = timezone.now() - timezone.timedelta(days=30)
#         # Se limiter aux commandes passées avant le début de la période actuelle et sans retrait futur
#         return CartItem.objects.filter(
#             product=obj,
#             order__order_date__gte=start_date,
#             order__order_date__lte=timezone.now(),
#             order__pick_up_date__lte=timezone.now()  # Exclure les commandes futures (retail des produits)
#         ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
#
#     def total_sales_last_6_months(self, obj):
#         # Calculer les ventes des 6 derniers mois, en comptant la quantité vendue
#         start_date = timezone.now() - timezone.timedelta(days=180)
#         # Se limiter aux commandes passées avant le début de la période actuelle et sans retrait futur
#         return CartItem.objects.filter(
#             product=obj,
#             order__order_date__gte=start_date,
#             order__order_date__lte=timezone.now(),
#             order__pick_up_date__lte=timezone.now()  # Exclure les commandes futures (retail des produits)
#         ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
#
#     def total_sales_future(self, obj):
#         # Calculer les ventes futures, en comptant la quantité vendue
#         now = timezone.now()
#         # Se limiter aux ventes dont la date de retrait est dans le futur
#         return CartItem.objects.filter(
#             product=obj,
#             order__pick_up_date__gte=now  # Inclure seulement les futures ventes (retrait à venir)
#         ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
#
#     total_sales_last_month.short_description = "Ventes des 30 derniers jours"
#     total_sales_last_6_months.short_description = "Ventes des 180 derniers jours"
#     total_sales_future.short_description = "Ventes futures"
#
#     def get_queryset(self, request):
#         # Récupérer le queryset de base
#         queryset = super().get_queryset(request)
#
#         # Annoter le queryset avec les données de ventes, en sommant les quantités pour chaque produit
#         queryset = queryset.annotate(
#             last_month_sales=Sum(
#                 'cartitem__quantity',
#                 filter=Q(cartitem__order__order_date__gte=timezone.now() - timezone.timedelta(days=30),
#                          cartitem__order__order_date__lte=timezone.now(),
#                          cartitem__order__pick_up_date__lte=timezone.now())
#             ),
#             last_6_months_sales=Sum(
#                 'cartitem__quantity',
#                 filter=Q(cartitem__order__order_date__gte=timezone.now() - timezone.timedelta(days=180),
#                          cartitem__order__order_date__lte=timezone.now(),
#                          cartitem__order__pick_up_date__lte=timezone.now())
#             ),
#             future_sales=Sum(
#                 'cartitem__quantity',
#                 filter=Q(cartitem__order__pick_up_date__gte=timezone.now())
#             )
#         ).order_by('-last_month_sales')  # Trier par les ventes du dernier mois
#
#         return queryset


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
    list_display = ('id', 'user', 'order_date', 'is_paid', "pick_up_date", 'total_price', 'get_cart_items')
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
