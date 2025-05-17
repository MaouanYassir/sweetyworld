from django.http import JsonResponse
from django.utils.timezone import make_aware, is_naive
from datetime import datetime, timedelta
from django.utils.translation import get_language
from shop.models import Order


def check_quota_index(request):
    date_str = request.GET.get('date')
    try:
        # Conversion de la date en datetime aware
        date = datetime.strptime(date_str, "%Y-%m-%d")
        pick_up_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        if is_naive(pick_up_date):
            pick_up_date = make_aware(pick_up_date)

        # Date minimale = aujourd'hui + 3 jours
        min_date = make_aware(datetime.now() + timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)

        # Détecter la langue
        lang = get_language()

        # Si la date est trop proche
        if pick_up_date < min_date:
            message = (
                f"Veuillez choisir une date à partir du {min_date.strftime('%d/%m/%Y')}."
                if lang == 'fr' else
                f"Kies een datum vanaf {min_date.strftime('%d/%m/%Y')}."
            )
            return JsonResponse({
                "available": False,
                "remaining": 0,
                "error": message
            })

        # Vérifier les commandes existantes à cette date
        orders_on_date = Order.objects.filter(pick_up_date=pick_up_date)
        total_quantity = sum(
            sum(item.quantity for item in order.order_items.all()) for order in orders_on_date
        )

        remaining = max(0, 30 - total_quantity)

        if remaining > 0:
            message = (
                f"✅ Il reste {remaining} gâteaux disponibles pour le {pick_up_date.strftime('%d/%m/%Y')}."
                if lang == 'fr' else
                f"✅ Er zijn nog {remaining} taarten beschikbaar op {pick_up_date.strftime('%d/%m/%Y')}."
            )
            return JsonResponse({
                "available": True,
                "remaining": remaining,
                "message": message
            })
        else:
            message = (
                "Le quota de 30 gâteaux est déjà atteint pour cette date."
                if lang == 'fr' else
                "Het quotum van 30 taarten is al bereikt voor deze datum."
            )
            return JsonResponse({
                "available": False,
                "remaining": 0,
                "error": message
            })

    except Exception:
        fallback = (
            "Date invalide." if get_language() == "fr" else "Ongeldige datum."
        )
        return JsonResponse({"available": False, "error": fallback}, status=400)