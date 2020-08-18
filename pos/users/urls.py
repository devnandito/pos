from django.urls import path
from pos.users.views import show_home, login_view, logout_view, show_user, create_user, create_profile, show_profile, edit_user, delete_user, edit_profile, set_pwd, change_pwd, delete_profile
from pos.levels.views import create_level_ajax

app_name = 'pos.users'

urlpatterns = [
    path('', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('dashboard/', show_home, name='home'),
    path('dashboard/users', show_user, name='show'),
    path('dashboard/create/user', create_user, name='create'),
    path('dashboard/edit/<int:pk>/user', edit_user, name='edit'),
    path('dashboard/delete/<int:pk>/user', delete_user, name='delete'),
    path('dashboard/set/<int:pk>/user', set_pwd, name='set'),
    path('dashboard/change/<int:pk>/user', change_pwd, name='change'),
    path('dashboard/create/user/profile', create_profile, name='createprofile'),
    path('dashboard/edit/user/<int:pk>/profile', edit_profile, name='editprofile'),
    path('dashboard/delete/user/<int:pk>/profile', delete_profile, name='deleteprofile'),
    path('dashboard/show/user/profile', show_profile, name='showprofile'),
    path('dashboard/create/user/ajax/get/level', create_level_ajax, name='getlevel'),
]