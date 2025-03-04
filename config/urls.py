# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path, include
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('shop.urls')),
#     path('accounts/', include('accounts.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
#



from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),  # L'admin ne sera pas traduit
] + i18n_patterns(
    path('', include('shop.urls')),  # Les URLs de l'app shop seront traduites
    path('accounts/', include('accounts.urls')),  # Les URLs de l'app accounts seront traduites
    path('i18n/', include('django.conf.urls.i18n')),  # Ajouter cette ligne
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#!!!!!!!!!!!!!!!!!!!!!!!! regler le problem de la page succes qui devient enfrançais et traduction de la page admin(produits et description)
#et du bouton de selection de langue qui ne fonctionne pas(je dois changer l'url manuellement')