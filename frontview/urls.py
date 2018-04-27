from django.urls import path

from . import views


app_name = "frontview"


urlpatterns = [
    path('', views.index, name="index"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
