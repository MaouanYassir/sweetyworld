
from django.shortcuts import render, redirect

from shop.models.ContactMessage import ContactMessage


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name,
                                      email=email,
                                      subject=subject,
                                      message=message)
        return redirect('home')  # Rediriger vers la page d'accueil après soumission du message
    return render(request, 'shop/contact.html')
