from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Shopper
from django.contrib.auth.decorators import login_required



def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = Shopper.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        login(request, user)

        # Redirection avec suppression des cookies de consentement
        response = redirect('home')
        response.delete_cookie('cookies_choice_made')
        response.delete_cookie('analytics')
        response.delete_cookie('stripe')
        response.delete_cookie('personalization')

        return response

    return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)

            # Redirection avec suppression des cookies de consentement
            response = redirect('home')
            response.delete_cookie('cookies_choice_made')
            response.delete_cookie('analytics')
            response.delete_cookie('stripe')
            response.delete_cookie('personalization')

            return response
        else:
            messages.error(request, "Email ou mot de passe incorrect")
            return render(request, 'accounts/signin.html')

    return render(request, 'accounts/signin.html')


def logout_user(request):
    # Déconnexion
    logout(request)

    # Supprimer la session (très utile)
    request.session.flush()

    # Rediriger vers la page d’accueil
    return redirect('home')




@login_required
def delete_account(request):
    user = request.user

    # Supprimer aussi les CartItem liés manuellement si nécessaire
    from shop.models import CartItem  # adapte ce chemin si ton app s'appelle différemment
    CartItem.objects.filter(cart__user=user).delete()

    # Supprime l'utilisateur (les Cart et Order seront supprimés automatiquement)
    user.delete()
    messages.success(request, "Votre compte et toutes vos données ont été supprimés avec succès.")
    return redirect('home')

# Create your views here.
