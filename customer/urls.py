from django.urls import path

from . import views


app_name = 'customer'


urlpatterns = [
    path('panel/<uuid:uuid>/', views.user_panel, name='user_panel'),

    path('panel/baskets/<uuid:uuid>/', views.user_baskets, name='user_baskets'),
    path('panel/orders/<uuid:uuid>/', views.user_orders, name='user_orders'),
    path('panel/favorites/<uuid:uuid>/', views.user_favorites, name='user_favorites'),
    path('panel/settings/<uuid:uuid>/', views.user_settings, name='user_settings'),

    path('panel/orders/order_pdf/<uuid:basket_code>/', views.order_pdf, name='order_pdf'),
]