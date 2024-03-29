from django.urls import path 
from customer.api import views

urlpatterns = [
    path('change_password/', views.change_password, name="change_password"),
    path('get_user_info/', views.get_user_info, name="get_user_info"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('edit_user/', views.edit_user, name="edit_user"),
    path('add_address/', views.add_address, name="add_address"),
    path('delete_address/', views.delete_address, name="delete_address"),
    path('get_addresses/', views.get_addresses, name="get_address"),
    path('add_comment/', views.add_comment, name="add_comment"),
    path('delete_comment/', views.delete_comment, name="delete_comment"),
    path('add_favorite/', views.add_favorite, name="add_favorite"),
    path('delete_favorite/', views.delete_favorite, name="delete_favorite"),
    path('get_favorites/', views.get_favorites, name="get_favorite"),
    # path('search_user/', views.user_search, name="user_search"),
    path('logout/', views.logout, name='logout'),
]
