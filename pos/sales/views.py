# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Models
from pos.sales.models import Sale

# Forms
from pos.sales.forms import SaleForm

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
    template = loader.get_template('sales/add.html')
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'form': form,
                'uri': get_url('sales'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = SaleForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('sales'),
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
                'form': form,
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