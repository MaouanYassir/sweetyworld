from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Shopper


def signup(request):
    # Si la requête est de type POST, cela signifie que l'utilisateur a soumis le formulaire d'inscription
    if request.method == "POST":
        # Récupération de l'email, du nom d'utilisateur et du mot de passe soumis via le formulaire
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Création d'un nouvel utilisateur avec les informations fournies
        user = Shopper.objects.create_user(email=email,
                                           username=username,
                                           password=password)

        # Connexion de l'utilisateur après la création de son compte
        login(request, user)

        # Redirection vers la page d'accueil après l'inscription
        return redirect('home')

    # Si la requête n'est pas de type POST, on affiche simplement la page d'inscription
    return render(request, 'accounts/signup.html')


def signin(request):
    # Si la requête est de type POST, cela signifie que l'utilisateur a soumis le formulaire de connexion
    if request.method == "POST":
        # Récupération de l'email et du mot de passe soumis via le formulaire (les noms des champs doivent correspondre)
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authentification de l'utilisateur avec l'email (USERNAME_FIELD défini dans le modèle comme 'email') et le mot de passe
        user = authenticate(request, username=email, password=password)

        # Si l'authentification a réussi (l'utilisateur existe et les informations sont correctes)
        if user:
            # Connexion de l'utilisateur (création de la session)
            login(request, user)
            # Redirection vers la page d'accueil (ou une autre page)
            return redirect('home')

        else:
            # Si l'authentification échoue, afficher un message d'erreur
            messages.error(request, "Email ou mot de passe incorrect")
            # Recharger la page de connexion avec le message d'erreur
            return render(request, 'accounts/signin.html')

    # Si la requête n'est pas de type POST (donc probablement GET), on affiche simplement la page de connexion
    return render(request, 'accounts/signin.html')


def logout_user(request):
    # Déconnexion de l'utilisateur
    logout(request)

    # Redirection vers la page d'accueil (ou une autre page de ton choix)
    return redirect('home')


# Create your views here.
