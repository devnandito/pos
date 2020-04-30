from django.urls import path
from pos.levels.views import show_level, create_level, create_level_ajax, edit_level, delete_level

app_name = 'pos.levels'

urlpatterns = [
    path('dashboard/create/level', create_level, name='create'),
    path('dashboard/edit/<int:pk>/level', edit_level, name='edit'),
    path('dashboard/delete/<int:pk>/level', delete_level, name='delete'),
    path('dashboard/show/level', show_level, name='show'),
    path('dashboard/create/ajax/get/level', create_level_ajax, name='getlevel'),
]