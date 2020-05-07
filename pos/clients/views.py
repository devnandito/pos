# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Models
from pos.clients.models import Client

# Forms
from pos.clients.forms import ClientForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Clientes', 'clientes', 'Cliente', 'cliente']
    return name

@login_required()
def show_client(request):
    tmp = get_name()
    list_title = ['#', 'Nombre', 'Apellido', 'Cedula', 'Email', 'Telefono', 'Dirección', 'Fecha cumpleaños', 'Compras', 'Acciones']
    template = loader.get_template('clients/show.html')
    object_list = Client.objects.all()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('clients'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_client(request):
    tmp = get_name()
    template = loader.get_template('clients/add.html')
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('clients'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ClientForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('clients'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_client(request, pk):
    tmp = get_name()
    template = loader.get_template('clients/edit.html')
    ins = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('clients'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ClientForm(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('clients'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_client(request, pk):
    tmp = get_name()
    template = loader.get_template('clients/delete.html')
    object_list = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('clients:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('clients'),
        }
    return HttpResponse(template.render(context, request))

@login_required()
def create_client_ajax(request):
    tmp = get_name()
    template = loader.get_template('clients/modal.html')
    if request.method == 'POST' and request.is_ajax():
        form = ClientForm(request.POST)
        if form.is_valid():
            data = form.save()
            client_info = {
                'id': data.id,
                'first_name': data.first_name,
            }
            return JsonResponse({'client_info' : client_info}, status=200)
        # else:
        #     return JsonResponse({'message': 'Error message'}, status=500)
    else:
        form = ClientForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
    }
    return HttpResponse(template.render(context, request))