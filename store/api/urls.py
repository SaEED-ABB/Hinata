from django.urls import path, include

from store.api import views

store_urlpatterns = [
    path('get_products/', views.get_products, name="get_products"),
    path('get_categories/', views.get_categories, name="get_categories"),
    path('add_to_basket/', views.add_to_basket, name="add_to_basket"),
    path('get_product_info/', views.get_product_info, name="get_product_info"),
]
