from django.urls import path
from pos.pages.views import show_home

app_name = 'pos.pages'

urlpatterns = [
    path('', show_home, name='show'),
]
