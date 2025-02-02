
from django.db import models



class ContactMessage(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" message de {self.name} - sujet: {self.subject}"


