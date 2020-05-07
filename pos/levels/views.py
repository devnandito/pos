# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Models
from pos.levels.models import Level

# Forms
from pos.levels.forms import LevelForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Niveles', 'niveles', 'Nivel', 'nivel']
    return name

@login_required()
def show_level(request):
    tmp = get_name()
    list_title = ['#', 'Descripción', 'Acciones']
    template = loader.get_template('levels/show.html')
    object_list = Level.objects.all()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('levels'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_level(request):
    tmp = get_name()
    template = loader.get_template('levels/add.html')
    if request.method == 'POST':
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('levels'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = LevelForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('levels'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_level(request, pk):
    tmp = get_name()
    template = loader.get_template('levels/edit.html')
    ins = get_object_or_404(Level, pk=pk)
    if request.method == 'POST':
        form = LevelForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('levels'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
            # return HttpResponseRedirect(reverse('levels:show'))
    else:
        form = LevelForm(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('levels'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_level(request, pk):
    tmp = get_name()
    template = loader.get_template('levels/delete.html')
    object_list = get_object_or_404(Level, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('levels:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('levels'),
        }
    return HttpResponse(template.render(context, request))

@login_required()
def create_level_ajax(request):
    tmp = get_name()
    template = loader.get_template('levels/modal.html')
    if request.method == 'POST' and request.is_ajax():
        form = LevelForm(request.POST)
        if form.is_valid():
            data = form.save()
            level_info = {
                'id': data.id,
                'description': data.description,
            }
            return JsonResponse({'level_info' : level_info}, status=200)
        # else:
        #     return JsonResponse({'message': 'Error message'}, status=500)
    else:
        form = LevelForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
    }
    return HttpResponse(template.render(context, request))