from django.urls import path

from . import views


app_name = 'store'


urlpatterns = [
    path('products/', views.products, name="products"),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:product_slug>/images/<slug:image_slug>/', views.product_image_detail, name='product_image_detail'),
]