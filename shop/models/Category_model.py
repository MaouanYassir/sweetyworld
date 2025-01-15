from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.CharField(max_length=120, blank=False, null=False)
    slug = models.SlugField(max_length=120, blank=False, null=False)
    image = models.ImageField(upload_to='images', blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name