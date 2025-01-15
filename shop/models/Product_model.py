from django.db import models

from shop.models.Category_model import Category


class Product(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    slug = models.SlugField(max_length=60, blank=False, null=False)
    image = models.ImageField(upload_to="images", blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
