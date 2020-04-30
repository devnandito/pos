from django.urls import path
from pos.products.views import show_product, create_product, delete_product, edit_product, show_product_json, show_product_json_post

app_name = 'pos.products'

urlpatterns = [
    path('dashboard/create/product', create_product, name='create'),
    path('dashboard/edit/<int:pk>/product', edit_product, name='edit'),
    path('dashboard/delete/<int:pk>/product', delete_product, name='delete'),
    path('dashboard/show/product', show_product, name='show'),
    path('dashboard/show/product/api/v1', show_product_json, name='showjson'),
    # path('dashboard/show/product/api/v2/<int:fkcategory>', show_product_json_get, name='showjsonget'),
    path('dashboard/show/product/api/v3', show_product_json_post, name='showjsonpost'),
]