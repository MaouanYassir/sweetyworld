from django.urls import path

from .views.category_view import category_view
from .views.Categories_view import categories_view
from .views.index_view import index_view

urlpatterns = [
    path('', index_view, name='index_view'),
    path('categories/', categories_view, name='categories_view'),
    path('category/<slug:slug>/', category_view, name='category_view'),
]