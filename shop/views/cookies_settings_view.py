from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def cookies_settings_view(request):
    if request.method == 'POST':
        response = redirect('home')

        # Durées RGPD (en secondes)
        analytics_duration = 60 * 60 * 24 * 30 * 13  # 13 mois
        stripe_duration = 60 * 60 * 24 * 30 * 24     # 24 mois
        personalization_duration = 60 * 60 * 24 * 30 * 6  # 6 mois

        # Consentement utilisateur
        analytics = 'analytics' in request.POST
        stripe = 'stripe' in request.POST
        personalization = 'personalization' in request.POST

        # Indique que l'utilisateur a fait un choix
        response.set_cookie('cookies_choice_made', 'true', max_age=analytics_duration)

        # Cookies facultatifs
        response.set_cookie('analytics', 'true' if analytics else 'false', max_age=analytics_duration)
        response.set_cookie('stripe', 'true' if stripe else 'false', max_age=stripe_duration)
        response.set_cookie('personalization', 'true' if personalization else 'false', max_age=personalization_duration)

        return response

    return render(request, 'shop/cookies_settings.html')
