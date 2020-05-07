# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json

# Models
from pos.sales.models import Sale
from pos.products.models import Product
from pos.users.models import User

# Forms
from pos.sales.forms import SaleForm, CustomSaleForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Ventas', 'ventas', 'Venta', 'venta']
    return name

@login_required()
def show_sale(request):
    tmp = get_name()
    list_title = ['#', 'Codigo', 'Cliente', 'Vendedor', 'Producto', 'Impuesto', 'Neto', 'Total', 'Metodo pago', 'Acciones']
    template = loader.get_template('sales/show.html')
    object_list = Sale.objects.all()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('sales'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_sale(request):
    tmp = get_name()
    template = loader.get_template('sales/addsales.html')
    list_title = ['#', 'Imagen', 'Descripción', 'Código', 'Stock',  'Acciones']
    if request.method == 'POST':
        # form = CustomSaleForm(request.POST)
        # form.fields['fkuser'].queryset = Sale.objects.filter(id=request.user.id)
        data_sale = {
            'newTax': request.POST['newPriceTax'],
            'net': request.POST['newPriceNet'],
        }
        message = 'Los datos se guardaron correctamente!'
        tpl = loader.get_template('sales/save.html')
        contextSuccess = {
            'title': get_body(tmp[3], tmp[0]),
            'uri': get_url('sales'),
            'message': message,
            'data_sale': data_sale,
        }
        return HttpResponse(tpl.render(contextSuccess, request))
        # if form.is_valid():
        #     form.save()
        #     data_sale = {
        #         'newTax': request.POST['newPriceTax'],
        #         'net': request.POST['newPriceNet'],
        #     }
        #     message = 'Los datos se guardaron correctamente!'
        #     tpl = loader.get_template('sales/save.html')
        #     contextSuccess = {
        #         'title': get_body(tmp[3], tmp[0]),
        #         'uri': get_url('sales'),
        #         'message': message,
        #         'data_sale': data_sale,
        #     }
        #     return HttpResponse(tpl.render(contextSuccess, request))
    else:
        object_list = Sale.objects.all().order_by('-invoice')
        if object_list:
            for item in object_list:
                num = item.invoice
        else:
            num = 10001 
        default_data = {
            'seller': request.user,
            'sellerid': request.user.id,
            'invoice': num,
        }
        form = CustomSaleForm(initial=default_data)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('sales'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_sale(request, pk):
    tmp = get_name()
    template = loader.get_template('sales/edit.html')
    ins = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('sales'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = SaleForm(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('sales'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_sale(request, pk):
    tmp = get_name()
    template = loader.get_template('sales/delete.html')
    object_list = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('sales:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('sales'),
        }
    return HttpResponse(template.render(context, request))

def print_format(value):
    value = str('{}'.format(value))
    return value

def print_uri_edit(value):
    value = str('../edit/{}/product'.format(value))
    return value

def print_uri_delete(value):
    value = str('../delete/{}/product'.format(value))
    return value

def print_uri_image(value):
    if value == '':
        value = '../../static/media/products/default/anonymous.png'
    else:
        value = value
    return value

def print_stock(value):
    if value <=10:
        value = '<button class="btn btn-danger">'+str(value)+'</button></td>'
    elif value > 11 and value <=15:
        value = '<button class="btn btn-warning">'+str(value)+'</button></td>'
    else:
        value = '<button class="btn btn-success">'+str(value)+'</button></td>'
    return value

@login_required()
def show_product_sale_json(request):
    object_list = Product.objects.all()
    data = [{
        '#': item.id,
        'Imagen': '<img class="img-circle" width="60px" src="'+print_uri_image(item.image.url)+'" alt=""/>',
        'Descripcion': item.description,
        'Codigo': item.code,
        'Precio compra': print_format(item.purchase_price),
        'Precio venta': print_format(item.sale_price),
        'Stock': print_stock(item.stock),
        'Acciones': '<div class="btn-group"><button class="btn btn-primary addProduct recoveryButton" idProduct="'+print_format(item.id)+'">Agregar</button></div>',
        } for item in object_list]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

@login_required()
def get_product_json_post(request):
    fkcategory = request.GET.get('idproduct', None)
    object_list = Product.objects.filter(id=fkcategory).order_by('-code')
    data = [{
        'id': item.id,
        'description': print_format(item.description),
        'stock': print_format(item.stock),
        'sale_price': print_format(item.sale_price),
        } for item in object_list]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

@login_required()
def get_product_json_post1(request):
    object_list = Product.objects.all()
    data = [{
        'id': item.id,
        'description': print_format(item.description),
        'stock': print_format(item.stock),
        'sale_price': print_format(item.sale_price),
        } for item in object_list]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")