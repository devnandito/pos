from django.urls import path
from pos.sales.views import show_sale, create_sale, edit_sale, delete_sale, show_product_sale_json, get_product_json_post, get_product_json_post1, invoice_pdf

app_name = 'pos.sales'

urlpatterns = [
    path('dashboard/create/sale', create_sale, name='create'),
    path('dashboard/edit/sale/<int:pk>', edit_sale, name='edit'),
    path('dashboard/edit/sale/api/v1', show_product_sale_json, name='salejson1'),
    path('dashboard/delete/<int:pk>/sale', delete_sale, name='delete'),
    path('dashboard/print/<int:pk>/sale', invoice_pdf, name='print'),
    path('dashboard/show/sale', show_sale, name='show'),
    path('dashboard/create/api/v1', show_product_sale_json, name='salejson'),
    path('dashboard/show/product/api/v4', get_product_json_post, name='getproduct'),
    path('dashboard/show/product/api/v5', get_product_json_post1, name='getproduct1'),
]