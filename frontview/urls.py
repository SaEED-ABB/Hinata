from django.urls import path

from frontview import views

urlpatterns = [
    path('', views.index, name="index"),
    path('products/', views.products, name="products"),
]
