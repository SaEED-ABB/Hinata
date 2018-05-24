from django.urls import path

from . import views


app_name = 'customer'


urlpatterns = [
    path('panel/<slug:slug>/', views.user_panel, name='user_panel')
]