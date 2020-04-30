from django.urls import path
from pos.sales.views import show_sale, create_sale, edit_sale, delete_sale

app_name = 'pos.sales'

urlpatterns = [
    path('dashboard/create/sale', create_sale, name='create'),
    path('dashboard/edit/<int:pk>/sale', edit_sale, name='edit'),
    path('dashboard/delete/<int:pk>/sale', delete_sale, name='delete'),
    path('dashboard/show/sale', show_sale, name='show'),
]