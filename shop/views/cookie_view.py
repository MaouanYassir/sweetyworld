from django.shortcuts import render


def cookies_policy(request):
    return render(request, 'shop/cookies.html')