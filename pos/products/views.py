# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
import random

# Models
from pos.products.models import Product

# Forms
from pos.products.forms import ProductForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Productos', 'productos', 'Producto', 'producto']
    return name

@login_required()
def show_product(request):
    tmp = get_name()
    list_title = ['#', 'Imagen', 'Descripción', 'Categoria', 'Código', 'Precio compra', 'Precio venta', 'Stock',  'Acciones']
    template = loader.get_template('products/show.html')
    # object_list = Product.objects.all()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        # 'object_list': object_list,
        'uri': get_url('products'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_product(request):
    tmp = get_name()
    template = loader.get_template('products/add.html')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            val1 = form.cleaned_data['sales_value']
            val2 = form.cleaned_data['purchase_price']
            res = float(val2) + (float(val2)*int(val1))/100
            pro = form.save(commit=False)
            pro.sale_price = res
            pro.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('products'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ProductForm()
    context = {
        'form': form,
        'title': get_body(tmp[3], tmp[0]),
        'uri': get_url('products'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_product(request, pk):
    tmp = get_name()
    template = loader.get_template('products/edit.html')
    ins = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=ins)
        if form.is_valid():
            val1 = form.cleaned_data['sales_value']
            val2 = form.cleaned_data['purchase_price']
            res = float(val2) + (float(val2)*int(val1))/100
            pro = form.save(commit=False)
            pro.sale_price = res
            pro.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('products'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        vi = float(ins.purchase_price)
        vf = float(ins.sale_price)
        restmp = vf - vi
        resf = (restmp/vi)*100
        val = int(resf)
        default_data = {
            'sales_value': val,
        }
        form = ProductForm(initial=default_data, instance=ins) # initial puede agregar todos los valores o solo uno
    context = {
        'form': form,
        'title': get_body(tmp[3], tmp[0]),
        'uri': get_url('products'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_product(request, pk):
    tmp = get_name()
    template = loader.get_template('products/delete.html')
    object_list = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('products:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('products'),
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
def show_product_json(request):
    object_list = Product.objects.all()
    if request.user.profile.level.id == 1:
        data = [{
            '#': item.id,
            'Imagen': '<img class="img-circle" width="60px" src="'+print_uri_image(item.image.url)+'" alt=""/>',
            'Descripcion': item.description,
            'Categoria': print_format(item.fkcategory.description),
            'Codigo': item.code,
            'Precio compra': print_format(item.purchase_price),
            'Precio venta': print_format(item.sale_price),
            'Stock': print_stock(item.stock),
            'Acciones': '<div class="btn-group"><a href="'+print_uri_edit(item.id)+'" class="btn btn-warning"><i class="fa fa-pencil"></i></a><a href="'+print_uri_delete(item.id)+'" class="btn btn-danger"><i class="fa fa-times"></i></a></div>',
            } for item in object_list]
    else:
        data = [{
            '#': item.id,
            'Imagen': '<img class="img-circle" width="60px" src="'+print_uri_image(item.image.url)+'" alt=""/>',
            'Descripcion': item.description,
            'Categoria': print_format(item.fkcategory.description),
            'Codigo': item.code,
            'Precio compra': print_format(item.purchase_price),
            'Precio venta': print_format(item.sale_price),
            'Stock': print_stock(item.stock),
            'Acciones': '<div class="btn-group"><a href="'+print_uri_edit(item.id)+'" class="btn btn-warning"><i class="fa fa-pencil"></i></a>',
            } for item in object_list]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

@login_required()
def show_product_json_post(request):
    fkcategory = request.GET.get('fkcategory', None)
    object_list = Product.objects.filter(fkcategory_id=fkcategory).order_by('-code')
    if object_list:
        data = [{
            'id': item.id,
            'categoria': print_format(item.fkcategory.id),
            'codigo': item.code,
            } for item in object_list]
    else:
        code = fkcategory+'01'
        data = [{'id':'null',' categoria':fkcategory, 'codigo':code}]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

def get_color1(value):
    color_list = ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc']
    value = color_list[value]
    return value

def get_digit(number):
    if number < 10:
        return number
    else:
        num = [0,1,2,3,4]
        value = random.choice(num)
        return value

@login_required()
def show_report_product_json(request):
    object_list = Product.objects.all().order_by('-sales')[:5]
    data_product = [{
        'value': item.sales,
        'color': get_color1(get_digit(int(item.id))),
        'highlight': get_color1(get_digit(int(item.id))),
        'label': item.description,

        } for item in object_list]
    return JsonResponse({'data_product': data_product}, status=200)

# @login_required()
# def show_product_json_get(request, fkcategory):
#     object_list = Product.objects.filter(fkcategory_id=fkcategory)
#     data = [{
#         '#': item.id,
#         'Descripcion': item.description,
#         'Categoria': print_format(item.fkcategory.description),
#         'Codigo': item.code,
#         'Precio compra': print_format(item.purchase_price),
#         'Precio venta': print_format(item.sale_price),
#         'Stock': item.stock,
#         } for item in object_list]
#     json_data = json.dumps(data)
#     return HttpResponse(json_data, content_type="application/json")

# def climaParam(request):
#     text = request.GET.get('text', None)
#     month = request.GET.get('month', None)
#     year = request.GET.get('year', None)
#     data = {
#         'city': text,
#         'month': month,
#         'year': year
#     }
#     return HttpResponse(json.dumps(data, ensure_ascii=False, encoding="utf-8"), content_type='application/json')

# def ClimaJson3(request, city, month, year):
#     object_list = Climatology.objects.filter(id_estacion_id__id_ciudad__nombre__icontains=city, fecha__month=month,  fecha__year=year).order_by('fecha')
#     data = [{'Letter': int(item.fecha.day), 'Freq': item.tmax} for item in object_list]
#     return HttpResponse(json.dumps(data, ensure_ascii=False, encoding="utf-8"), content_type='application/json')

# @login_required()
# def show_product_json(request):
#     object_list = Product.objects.all()
#     json_data = serializers.serialize('json', object_list)
#     return HttpResponse(json_data, content_type="application/json")

# def show_product_json1(request):
#     object_list = Product.objects.all()
#     tmp = []
#     for i, c in enumerate(object_list):
#         i+=1
#         tmp.append([
#             (i),
#             (print_format(c.image)),
#             (c.code),
#             (c.description),
#             (c.fkcategory.description),
#             (c.stock),
#             (print_format(c.purchase_price)),
#             (print_format(c.sale_price)),
#             (c.stock),
#         ])
#     data = {'data': tmp}
#     json_data = json.dumps(data)
#     return HttpResponse(json_data, content_type="application/json")