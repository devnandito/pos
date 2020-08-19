from django import template
from decimal import Decimal

import re
import datetime
register = template.Library()

list_label = {
    'Description': ['Descripción', 'fa fa-address-card-o'],
    'Username': ['Usuario', 'fa fa-user'],
    'User': ['Usuario', 'fa fa-user'],
    'First name': ['Nombre', 'fa fa-child'],
    'Last name': ['Apellido', 'fa fa-child'],
    'Email address': ['Email', 'fa fa-envelope'],
    'Email': ['Email', 'fa fa-envelope'],
    'Password': ['Password', 'fa fa-lock'],
    'Password confirmation': ['Confirmar password', 'fa fa-lock'],
    'Old password': ['Password anterior', 'fa fa-lock'],
    'New password': ['Nuevo password', 'fa fa-lock'],
    'New password confirmation': ['Confirmacion nuevo password', 'fa fa-lock'],
    'Level': ['Nivel', 'fa fa-users'],
    'Active': ['Activo', 'fa fa-toggle-on'],
    'Profile picture': ['Foto', 'fa fa-file-image-o'],
    'Ci': ['Cedula', 'fa fa-id-card'],
    'Phone': ['Teléfono', 'fa fa-phone'],
    'Direction': ['Dirección', 'fa fa-address-card'],
    'Birthday': ['Fecha de nacimiento', 'fa fa-birthday-cake'],
    'Fkcategory': ['Categoria', 'fa fa-bars'],
    'Code': ['Codigo', 'fa fa-barcode'],
    'Invoice': ['Factura', 'fa fa-barcode'],
    'Image': ['Imagen', 'fa fa-file-image-o'],
    'Stock': ['Stock', 'fa fa-cc'],
    'Purchase price': ['Precion de compra', 'fa fa-money'],
    'Sales value': ['Precion de venta', 'fa fa-money'],
    'Fkclient': ['Cliente', 'fa fa-child'],
    'Fkuser': ['Usuario', 'fa fa-user'],
    'Seller': ['Vendedor', 'fa fa-user'],
    'Product': ['Producto', 'fa fa-product-hunt'],
    'Net': ['Neto', 'fa fa-money'],
    'Total': ['Total', 'fa fa-money'],
    'Payment': ['Metodo de pago', 'fa fa-money'],
    'Tax': ['Impuesto', 'fa fa-line-chart'],
}

@register.filter
def replace(value, arg):
    for k, v in list_label.items():
        if k == value:
            return v[arg]

def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg
    try:
        return int(arg)
    except ValueError:
        return float(arg)

@register.filter
def sum(value, arg):
    """Subtracts the arg from the value. """
    try:
        return valid_numeric(value) + valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ' '
sum.is_safe = False

@register.filter
def percent(value, arg):
    """Calcule percent the arg from the value. """
    try:
        return int((valid_numeric(value)*100) / valid_numeric(arg))
    except (ValueError, TypeError):
        try:
            return (value*100) / arg
        except Exception:
            return ' '
percent.is_safe = False

@register.filter
def sub(value, arg):
    """Subtracts the arg from the value. """
    try:
        return valid_numeric(value) - valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ' '
sub.is_safe = False

# list1 = {
#     '<label for="id_username">Username:</label>': 'Username:',
#     '<label for="id_first_name">First name:</label>': 'Nombre:',
#     '<label for="id_last_name">Last name:</label>': 'Apellido:',
#     '<label for="id_email">Email address:</label>': 'Email:',
#     '<label for="id_password">Password:</label>': 'Password:',
#     '<label for="id_password1">Password:</label>': 'Password:',
#     '<label for="id_password2">Password confirmation:</label>': 'Confirmar Password:',
#     '<label for="id_level">Level:</label>': 'Nivel:',
#     '<label for="id_description">Description:</label>': 'Descripción:',
#     '<label for="id_user">User:</label>': 'Usuario:',
#     '<label for="id_picture">Profile picture:</label>': 'Imagen:',
#     '<label for="id_old_password">Old password:</label>': 'Password actual:',
#     '<label for="id_new_password1">New password:</label>': 'Nuevo password:',
#     '<label for="id_new_password2">New password confirmation:</label>': 'Confirmar password:',
#     '<label for="id_is_active">Active:</label>': 'Activo:',
#     '<label for="id_fkcategory">Fkcategory:</label>': 'Categoria:',
#     '<label for="id_code">Code:</label>': 'Código:',
#     '<label for="id_image">Image:</label>': 'Imagen:',
#     '<label for="id_stock">Stock:</label>': 'Stock:',
#     '<label for="id_purchase_price">Purchase price:</label>': 'Precio compra:',
#     '<label for="id_sale_price">Sale price:</label>': 'Precio venta:',
#     '<label for="id_fkcategory">Fkcategory:</label>': 'Categoria:',
#     '<label for="id_sales">Sales:</label>': 'Venta:',
#     '<label for="id_sales_value">Sales value:</label>': 'Precio de venta:',
#     '<label for="id_ci">Ci:</label>': 'Cedula:',
#     '<label for="id_email">Email:</label>': 'Email:',
#     '<label for="id_phone">Phone:</label>': 'Telefono:',
#     '<label for="id_direction">Direction:</label>': 'Direccion:',
#     '<label for="id_birthday">Birthday:</label>': 'Fecha de nacimiento:',
#     '<label for="id_purchases">Purchases:</label>': 'Compras:',
#     '<label for="id_fkclient">Fkclient:</label>': 'Cliente:',
#     '<label for="id_fkuser">Fkuser:</label>': 'Vendedor:',
#     '<label for="id_product">Product:</label>': 'Producto:',
#     '<label for="id_tax">Tax:</label>': 'Impuesto:',
#     '<label for="id_net">Net:</label>': 'Neto:',
#     '<label for="id_total">Total:</label>': 'Total:',
#     '<label for="id_payment">Payment:</label>': 'Metodo pago:',
#     '<label for="id_invoice">Invoice:</label>': 'Factura:',
# }

# list2 = {
#     '<label for="id_username">Username:</label>': 'id_username',
#     '<label for="id_first_name">First name:</label>': 'id_first_name',
#     '<label for="id_last_name">Last name:</label>': 'id_last_name',
#     '<label for="id_email">Email address:</label>': 'id_email',
#     '<label for="id_password">Password:</label>': 'id_password',
#     '<label for="id_password1">Password:</label>': 'id_password1',
#     '<label for="id_password2">Password confirmation:</label>': 'id_password2',
#     '<label for="id_level">Level:</label>': 'id_level',
#     '<label for="id_description">Description:</label>': 'id_description',
#     '<label for="id_user">User:</label>': 'id_user',
#     '<label for="id_picture">Profile picture:</label>': 'id_picture',
#     '<label for="id_old_password">Old password:</label>': 'id_old_password',
#     '<label for="id_new_password1">New password:</label>': 'id_new_password1',
#     '<label for="id_new_password2">New password confirmation:</label>': 'id_new_password2',
#     '<label for="id_is_active">Active:</label>': 'id_is_active',
#     '<label for="id_code">Code:</label>': 'id_code',
#     '<label for="id_image">Image:</label>': 'id_image',
#     '<label for="id_stock">Stock:</label>': 'id_stock',
#     '<label for="id_purchase_price">Purchase price:</label>': 'id_purchase_price',
#     '<label for="id_sales">Sales:</label>': 'id_sales',
#     '<label for="id_sales_value">Sales value:</label>': 'id_sales_value',
#     '<label for="id_ci">Ci:</label>': 'id_ci',
#     '<label for="id_email">Email:</label>': 'id_email',
#     '<label for="id_phone">Phone:</label>': 'id_phone',
#     '<label for="id_direction">Direction:</label>': 'id_direction',
#     '<label for="id_birthday">Birthday:</label>': 'id_birthday',
#     '<label for="id_purchases">Purchases:</label>': 'id_purchases',
#     '<label for="id_fkclient">Fkclient:</label>': 'id_fkclient',
#     '<label for="id_fkuser">Fkuser:</label>': 'id_fkuser',
#     '<label for="id_product">Product:</label>': 'id_product',
#     '<label for="id_tax">Tax:</label>': 'id_tax',
#     '<label for="id_net">Net:</label>': 'id_net',
#     '<label for="id_total">Total:</label>': 'id_total',
#     '<label for="id_payment">Payment:</label>': 'id_payment',
#     '<label for="id_invoice">Invoice:</label>': 'id_invoice',
# }

# list3 = {
#     'Username':'fa fa-user',
#     'User':'fa fa-user',
#     'First name':'fa fa-child',
#     'Last name': 'fa fa-child',
#     'Email address': 'fa fa-envelope',
#     'Email': 'fa fa-envelope',
#     'Password': 'fa fa-lock',
#     'Password confirmation': 'fa fa-lock',
#     'Description': 'fa fa-address-card-o',
#     'Level': 'fa fa-users',
#     'Active': 'fa fa-toggle-on',
#     'Profile picture': 'fa fa-file-image-o',
#     'Ci': 'fa fa-id-card',
#     'Phone': 'fa fa-phone',
#     'Direction': 'fa fa-address-card',
#     'Birthday': 'fa fa-birthday-cake',
#     'Fkcategory': 'fa fa-bars',
#     'Code': 'fa fa-barcode',
#     'Image': 'fa fa-file-image-o',
#     'Stock': 'fa fa-cc',
#     'Purchase price': 'fa fa-money',
#     'Sales value': 'fa fa-money',
# }

# list4 = {
#     'Description':'Descripción',
#     'Username':'Usuario',
#     'User':'Usuario',
#     'First name':'Nombre',
#     'Last name':'Apellido',
#     'Email address':'Email',
#     'Email':'Email',
#     'Password': 'Password',
#     'Password confirmation': 'Confirmar password',
#     'Level': 'Nivel',
#     'Ci': 'Cedula',
#     'Phone': 'Teléfono',
#     'Direction': 'Dirección',
#     'Birthday': 'Fecha de nacimiento',
#     'Fkcategory': 'Categoría',
#     'Code': 'Código',
#     'Image': 'Imagen',
#     'Stok': 'Stock',
#     'Purchase price': 'Precio de compra',
#     'Sales value': 'Precio de venta',
# }

# @register.filter
# def replace1(arg):
#     for key, value in list1.items():
#         if arg == key:
#             return value

# @register.filter
# def replace2(arg):
#     for key, value in list2.items():
#         if arg == key:
#             return value

# @register.filter
# def replace3(arg):
#     for key, value in list3.items():
#         if arg == key:
#             return value

# @register.filter
# def replace4(arg):
#     for key, value in list4.items():
#         if arg == key:
#             return value

# @register.filter
# def viewHidden(arg):
#     now = datetime.datetime.now()
#     x = re.search(r'\"\d*\"', str(arg))
#     if x:
#         return x.group()
#     else:
#         return now


# @register.filter
# def getLevel(arg):
#     emp = Employee.objects.get(fkuser__username=arg)
#     return emp.fkposition.description

# @register.filter
# def place_value(arg):
#     return ("{:,}".format(arg))


# @register.filter
# def sumAmount(arg_list):
#     for i in arg_list:
#         suma =  suma + i.amount
#     return suma
