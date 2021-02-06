from django.urls import path
from pos.sales.views import show_sale, create_sale, edit_sale, delete_sale, show_report, show_product_sale_json, get_product_json_post, get_product_json_post1, invoice_pdf, show_report_sale_json

app_name = 'pos.sales'

urlpatterns = [
    path('dashboard/create/sale', create_sale, name='create'),
    path('dashboard/create/sale/api/v4', get_product_json_post, name='getproduct2'),
    path('dashboard/create/sale/api/v5', get_product_json_post1, name='getproduct3'),
    # path('dashboard/edit/<int:pk>/api/v4', get_product_json_post, name='getproduct4'),
    # path('dashboard/edit/sale/api/v5', get_product_json_post1, name='getproduct5'),
    path('dashboard/edit/sale/<int:pk>', edit_sale, name='edit'),
    path('dashboard/edit/sale/api/v1', show_product_sale_json, name='salejson1'),
    path('dashboard/delete/<int:pk>/sale', delete_sale, name='delete'),
    path('dashboard/print/<int:pk>/sale', invoice_pdf, name='print'),
    path('dashboard/show/sale', show_sale, name='show'),
    path('dashboard/show/report', show_report, name='report'),
    path('dashboard/create/api/v1', show_product_sale_json, name='salejson'),
    path('dashboard/show/product/api/v4', get_product_json_post, name='getproduct'),
    path('dashboard/show/product/api/v5', get_product_json_post1, name='getproduct1'),
    path('dashboard/show/report/api/v6', show_report_sale_json, name='sale_report'),
]
