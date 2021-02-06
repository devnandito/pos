# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

# Models
from pos.products.models import Product

# Forms

# Utilities
from pos.utils.functions import get_url, get_body

# Python
import datetime

def get_name():
    name = ['Pagina']
    return name

def show_home(request):
    template = loader.get_template('pages/show.html')
    tmp = get_name()
    # request.session["s_text"] = ''

    if request.method == 'POST':
        pass
        # form = FormSearch(request.POST)
        # if form.is_valid():
        #     search = request.POST['text']
        #     request.session['s_text'] = search
        #     product_list = Product.objects.filter(description=search)
        #     context = {
        #         'title': get_body(tmp[0], tmp[0]),
        #         'object_list': product_list,
        #     }
        #     return HttpResponse(template.render(context, request))
    else:
        pass
        # form = FormSearch()
    
    product_paginator = Product.objects.filter(Q(fkcategory=7)|Q(fkcategory=8))
    paginator = Paginator(product_paginator, 9)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        object_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)
    
    context = {
        'title': get_body(tmp[0], tmp[0]),
        'object_list': object_list,
    }
    return HttpResponse(template.render(context, request))
