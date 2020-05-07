from django.urls import path
from pos.clients.views import show_client, create_client, edit_client, delete_client, create_client_ajax

app_name = 'pos.clients'

urlpatterns = [
    path('dashboard/create/client', create_client, name='create'),
    path('dashboard/edit/<int:pk>/client', edit_client, name='edit'),
    path('dashboard/delete/<int:pk>/client', delete_client, name='delete'),
    path('dashboard/show/client', show_client, name='show'),
    path('dashboard/create/ajax/get/client', create_client_ajax, name='getclient'),
]