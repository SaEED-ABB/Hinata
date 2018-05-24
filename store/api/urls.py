from django.urls import path, include

from store.api import views

urlpatterns = [
    path('get_products/', views.get_products, name="get_products"),
    path('get_categories/', views.get_categories, name="get_categories"),
    path('add_to_basket/', views.add_to_basket, name="add_to_basket"),
    path('remove_from_basket/', views.remove_from_basket, name='remove_from_basket'),
    path('get_product_info/', views.get_product_info, name="get_product_info"),
    path('get_next_prev_of_product/', views.get_next_prev_of_product, name="get_next_prev_of_product"),
    path('get_history/', views.get_basket_history, name="get_basket_history"),
    path('search_product/', views.search_product, name="search_product"),
    path('get_active_basket_info/', views.get_active_basket_info, name='get_active_basket_info'),
]
