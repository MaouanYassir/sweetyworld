from django.db import models
from django.db.models import Sum
from shop.models.category_model import Category


class Product(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, default="")
    description = models.TextField(blank=False, null=False, default="")
    name_nl = models.CharField(max_length=60, blank=False, null=False, default="")
    description_nl = models.TextField(blank=False, null=False, default="")
    slug = models.SlugField(max_length=60, blank=False, null=False)
    image = models.ImageField(upload_to="images", blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name