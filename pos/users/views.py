# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

# Models
from pos.users.models import User, Profile
from pos.sales.models import Sale
from pos.categories.models import Category
from pos.clients.models import Client
from pos.products.models import Product

# Forms
from pos.users.forms import CustomUserCreationForm, ProfileForm, ProfileUserForm, CustomUserChangeForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Usuarios', 'usuarios', 'Usuario', 'usuario', 'Perfiles', 'perfiles', 'Perfil', 'perfil', 'Dashboard', 'password']
    return name

# Python
import datetime

@login_required()
def show_home(request):
    tmp = get_name()
    query1 = Sale.objects.all().aggregate(Sum('net'))
    query2 = Category.objects.count()
    query3 = Client.objects.count()
    query_init = Product.objects.all()
    query4 = query_init.count()
    query5 = query_init.order_by('-id')[:5]
    query6 = query_init.aggregate(Sum('sales'))
    query7 = query_init.order_by('-sales')[:4]
    template = loader.get_template('users/dashboard.html')
    context = {
        'title': get_body(tmp[8], tmp[8]),
        'total_sales': query1,
        'total_category': query2,
        'total_client': query3,
        'total_product': query4,
        'product_list': query5,
        'product_sum': query6,
        'product_list1': query7,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def show_user(request):
    tmp = get_name()
    list_title = ['#', 'Usuario', 'Email', 'Nombre', 'Apellido', 'Foto', 'Perfil', 'Estado', 'Ultimo login', 'Acciones']
    template = loader.get_template('users/show.html')
    object_list = User.objects.all()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('users'),
        'list_title':list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_user(request):
    tmp = get_name()
    template = loader.get_template('users/add.html')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        form1 = ProfileUserForm(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomUserCreationForm()
        form1 = ProfileUserForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'form1': form1,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))


@login_required()
def edit_user(request, pk):
    tmp = get_name()
    template = loader.get_template('users/edit.html')
    ins = get_object_or_404(User, pk=pk)
    ins1 = get_object_or_404(Profile, user=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=ins)
        form1 = ProfileUserForm(request.POST, request.FILES,  instance=ins1)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomUserChangeForm(instance=ins)
        form1 = ProfileUserForm(instance=ins1)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'form1': form1,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_user(request, pk):
    tmp = get_name()
    template = loader.get_template('users/delete.html')
    object_list = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('users:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('users'),
        }
    return HttpResponse(template.render(context, request))

@login_required()
def set_pwd(request, pk):
    tmp = get_name()
    template = loader.get_template('users/changepwd.html')
    ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = SetPasswordForm(ins, request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = SetPasswordForm(ins)
    context = {
        'title': get_body(tmp[9], tmp[9]),
        'form': form,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def change_pwd(request, pk):
    tmp = get_name()
    template = loader.get_template('users/changepwd.html')
    ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(ins, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = PasswordChangeForm(ins)
    context = {
        'title': get_body(tmp[9], tmp[9]),
        'form': form,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def show_profile(request):
    tmp = get_name()
    list_title = ['#', 'Usuario', 'Descripción', 'Perfil', 'Foto', 'Acciones']
    template = loader.get_template('profiles/show.html')
    object_list = Profile.objects.all()
    context = {
        'title': get_body(tmp[7], tmp[4]),
        'object_list': object_list,
        'uri': get_url('users'),
        'list_title':list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_profile(request):
    tmp = get_name()
    template = loader.get_template('profiles/add.html')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[7], tmp[4]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ProfileForm()
    context = {
        'title': get_body(tmp[7], tmp[4]),
        'form': form,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_profile(request, pk):
    tmp = get_name()
    template = loader.get_template('profiles/edit.html')
    ins = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, request.FILES, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[7], tmp[4]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ProfileUserForm(instance=ins)
    context = {
        'title': get_body(tmp[7], tmp[4]),
        'form': form,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_profile(request, pk):
    tmp = get_name()
    template = loader.get_template('profiles/delete.html')
    object_list = get_object_or_404(Profile, user=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('users:showprofile'))
    else:
        context = {
            'title': get_body(tmp[7], tmp[4]),
            'object_list': object_list,
            'uri': get_url('users'),
        }
    return HttpResponse(template.render(context, request))

def login_view(request):
    tmp = get_name()
    template = loader.get_template('users/login.html')
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse('users:show'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.get(user=user.id)
                profile.last_login = datetime.datetime.now()
                profile.save()
                return HttpResponseRedirect(reverse('users:home'))
            else:
                form = AuthenticationForm()
                text = 'El usuario esta inactivo'
                contextNoActive = {
                    'title': get_body(tmp[8], tmp[8]),
                    'text': text,
                    'form': form,
                }
                return HttpResponse(template.render(contextNoActive, request))
                # return HttpResponse("Tu cuenta esta inactiva.")
        else:
            form = AuthenticationForm()
            text = 'El usuario o la contraseña son incorrectas'
            contextNoUser = {
                'title': get_body(tmp[8], tmp[8]),
                'text': text,
                'form': form,
            }
            return HttpResponse(template.render(contextNoUser, request))
    else:
        form = AuthenticationForm()
    text = ''
    context = {
        'title': get_body(tmp[8], tmp[8]),
        'form': form,
        'text': text,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

# @login_required()
# def add_user(request):
#     title = 'Agregar usuario'
#     template = loader.get_template('users/add.html')
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:show'))
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form': form,
#         'title': title,
#     }
#     return HttpResponse(template.render(context, request))

# @login_required()
# def edit_user(request, pkuser, pkemployee):
#     title = 'Editar Usuario'
#     template = loader.get_template('employees/register.html')
#     ins = get_object_or_404(User, pk=pkuser)
#     ins1 = get_object_or_404(Employee, pk=pkemployee)
#     if request.method == 'POST':
#         form = SignUpEditForm(request.POST, instance=ins)
#         form1 = EmployeeForm(request.POST, instance=ins1)
#         if form.is_valid() and form1.is_valid():
#             form.save()
#             form1.save()
#             return HttpResponseRedirect(reverse('employees:showemployee'))
#     else:
#         form = SignUpEditForm(instance=ins)
#         form1 = EmployeeForm(instance=ins1)
#     context = {
#         'form': form,
#         'form1': form1,
#         'title': title,
#     }
#     return HttpResponse(template.render(context, request))

# @login_required()
# def create_user_ajax(request):
#     title = 'Agregar usuario'
#     template = loader.get_template('users/modal.html')
#     if request.method == 'POST' and request.is_ajax():
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             data = form.save()
#             user_info = {
#                 'id': data.id,
#                 'username': data.username,
#                 'email': data.email,
#                 'first_name': data.first_name,
#                 'last_name': data.last_name,
#             }
#             return JsonResponse({'user_info' : user_info}, status=200)
#         # else:
#         #     return JsonResponse({'message': 'Error message'}, status=500)
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form': form,
#         'title': title,
#     }
#     return HttpResponse(template.render(context, request))
