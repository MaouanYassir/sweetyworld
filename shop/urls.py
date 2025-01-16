from django.urls import path

from .views.Categories_view import categories_view
from .views.index_view import index_view

urlpatterns = [
    path('', index_view, name='index_view'),
    path('categories/', categories_view, name='categories_view'),
]