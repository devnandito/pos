# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Models
from pos.categories.models import Category

# Forms
from pos.categories.forms import CategoryForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Categorias', 'categorias', 'Categoria', 'categoria']
    return name

@login_required()
def show_category(request):
    tmp = get_name()
    list_title = ['#', 'Descripción', 'Acciones']
    template = loader.get_template('categories/show.html')
    object_list = Category.objects.all()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('categories'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_category(request):
    tmp = get_name()
    template = loader.get_template('categories/add.html')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'form': form,
                'uri': get_url('categories'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CategoryForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('categories'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_category(request, pk):
    tmp = get_name()
    template = loader.get_template('categories/edit.html')
    ins = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'form': form,
                'uri': get_url('categories'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CategoryForm(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('categories'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_category(request, pk):
    tmp = get_name()
    template = loader.get_template('categories/delete.html')
    object_list = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('categories:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('categories'),
        }
    return HttpResponse(template.render(context, request))