from django.urls import path
from pos.categories.views import show_category, create_category, edit_category, delete_category

app_name = 'pos.categories'

urlpatterns = [
    path('dashboard/create/category', create_category, name='create'),
    path('dashboard/edit/<int:pk>/category', edit_category, name='edit'),
    path('dashboard/delete/<int:pk>/category', delete_category, name='delete'),
    path('dashboard/show/category', show_category, name='show'),
]