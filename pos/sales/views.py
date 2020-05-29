# coding=utf-8

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

# generate pdf
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, landscape, portrait, A4
import urllib
#import StringIO
import PIL.Image

# Models
from pos.sales.models import Sale
from pos.products.models import Product
from pos.users.models import User
from pos.clients.models import Client

# Forms
from pos.sales.forms import SaleForm, CustomSaleForm, CustomEditSaleForm

# Utilities
from pos.utils.functions import get_url, get_body

def get_name():
    name = ['Ventas', 'ventas', 'Venta', 'venta']
    return name

@login_required()
def show_sale(request):
    tmp = get_name()
    list_title = ['#', 'Codigo', 'Cliente', 'Vendedor', 'Impuesto', 'Neto', 'Total', 'Metodo pago', 'Fecha', 'Acciones']
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
    list_title = ['#', 'Imagen', 'Descripción', 'Código', 'Stock', 'Acciones']
    if request.method == 'POST':
        form = CustomSaleForm(request.POST)
        if form.is_valid():
            invoice = form.cleaned_data['invoice']
            client = get_object_or_404(Client, pk=form.cleaned_data['fkclient'])
            seller = get_object_or_404(User, pk=form.cleaned_data['sellerid'])
            products = request.POST['listProduct']
            newTax = request.POST['newPriceTax']
            net = request.POST['newPriceNet']
            total = request.POST['totalSale']
            methodpay = request.POST['listMethodPay']
            data_product = json.loads(products)
            # list_product = []
            # list_product.append(item['count'])
            sum_total = 0
            for item in data_product:
                pro = get_object_or_404(Product, pk=item['id'])
                pro.stock = item['stock']
                pro.sales = int(pro.sales) + int(item['count'])
                pro.save()
                sum_total = int(sum_total) + int(item['count'])
            client.purchases = int(client.purchases) + int(sum_total)
            client.save()
            Sale.objects.create(
                invoice=invoice,
                fkclient=client,
                fkuser=seller,
                product=products,
                tax=newTax,
                net=net,
                total=total,
                payment=methodpay
                )
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('sales/save.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('sales'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        object_list = Sale.objects.all().order_by('invoice')
        if object_list:
            for item in object_list:
                num = item.invoice
            num = num + 1
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
    template = loader.get_template('sales/editsales.html')
    list_title = ['#', 'Imagen', 'Descripción', 'Código', 'Stock', 'Acciones']
    if request.method == 'POST':
        form = CustomEditSaleForm(request.POST)
        if form.is_valid():
            sale = get_object_or_404(Sale, invoice=form.cleaned_data['invoice'])
            client = get_object_or_404(Client, pk=form.cleaned_data['fkclient'])
            last_purchases = client.purchases
            seller = get_object_or_404(User, pk=form.cleaned_data['sellerid'])
            products = json.loads(sale.product)
            sum_total = 0
            for item in products:
                pro = get_object_or_404(Product, pk=item['id'])
                last_stock = pro.stock
                pro.stock = int(pro.stock) + int(item['count'])
                pro.sales = int(pro.sales) - int(item['count'])
                pro.save()
                sum_total = int(sum_total) + int(item['count'])
            client.purchases = int(client.purchases) - int(sum_total)
            client.save()
            invoice = form.cleaned_data['invoice']
            methodpay = request.POST['listMethodPay']
            sum_total1 = 0
            if request.POST['listProduct'] == "":
                data_product = products
                product_list = sale.product
                newTax = sale.tax
                net = sale.net
                total = sale.total
                for item in data_product:
                    pro = get_object_or_404(Product, pk=item['id'])
                    pro.sales = int(pro.sales) + int(item['count'])
                    pro.stock = last_stock
                    pro.save()
                client.purchases = last_purchases
                client.save()
            else:
                newTax = request.POST['newPriceTax']
                net = request.POST['newPriceNet']
                total = request.POST['totalSale']
                product_list = request.POST['listProduct']
                data_product = json.loads(product_list)
                for item in data_product:
                    pro = get_object_or_404(Product, pk=item['id'])
                    pro.stock = int(item['stock'])
                    pro.sales = int(pro.sales) + int(item['count'])
                    pro.save()
                    sum_total1 = int(sum_total1) + int(item['count'])
                client.purchases = int(client.purchases) + int(sum_total1)
                client.save()
            sale.invoice = invoice
            sale.fkclient = client
            sale.fkuser = seller
            sale.product = product_list
            sale.tax = newTax
            sale.net = net
            sale.total = total
            sale.payment = methodpay
            sale.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('sales/save.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('sales'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        object_list = Sale.objects.get(pk=pk)
        fkclient = object_list.fkclient.id
        nameclient = object_list.fkclient.first_name + ' ' + object_list.fkclient.last_name
        data_product = json.loads(object_list.product)
        percent = int(object_list.tax * 100) / int(object_list.net)
        default_data = {
            'seller': object_list.fkuser.first_name,
            'sellerid': object_list.fkuser.id,
            'invoice': object_list.invoice,
            'fkclient': fkclient,
            'nameclient': nameclient,
            'new_total_sale': object_list.total,
            'new_tax_sale': int(percent),
        }
        # form = CustomEditSaleForm(initial=default_data, fkclient=fkclient)
        form = CustomEditSaleForm(initial=default_data)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('sales'),
        'list_title': list_title,
        'data_product': data_product,
        'net': object_list.net,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_sale(request, pk):
    tmp = get_name()
    template = loader.get_template('sales/delete.html')
    object_list = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        products = json.loads(object_list.product)
        sum_purchases = 0
        for item in products:
            pro = get_object_or_404(Product, pk=item['id'])
            pro.stock = int(pro.stock) + int(item['count'])
            pro.sales = int(pro.sales) - int(item['count'])
            pro.save()
            sum_purchases = int(sum_purchases) + int(item['count'])
        object_list.delete()
        cli = get_object_or_404(Client, pk=object_list.fkclient.id)
        cli.purchases = int(cli.purchases) - int(sum_purchases)
        cli.save()
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

@login_required()
def invoice_pdf(request, pk):
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        pagesize=landscape(letter))
    # Our container for 'Flowable' objects
    elements = []
    # logo = "/var/www/html/pos/static/img/pdf/logo-negro-bloque.png"
    logo = settings.MEDIA_ROOT+'/static/img/pdf/logo-negro-bloque.png'
    im = Image(logo, 3*inch, 2*inch)

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    title = styles['Heading1']
    title.alignment=TA_CENTER
    thead = styles["Normal"]
    thead.alignment=TA_CENTER
    tbody = styles["BodyText"]
    tbody.alignment=TA_LEFT
    styles.wordWrap = 'CJK'
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_JUSTIFY))
    elements.append(im)

    elements.append(Paragraph('FACTURA', title))

    # Need a place to store our table rows
    table_data = []
    table_data.append([
        Paragraph(str('Factura.'), thead),
        Paragraph(str('Cliente'), thead),
        Paragraph(str('Productos'), thead),
        ])
    sales = Sale.objects.filter(invoice=pk)
    for c in sales:
        # Add a row to the table
        table_data.append([
            Paragraph(str(c.invoice), tbody),
            Paragraph(str(c.fkclient), tbody),
            Paragraph(str(c.product), tbody),
            ])
    
    # Create the table
    sale_table = Table(table_data, colWidths=[doc.width/8.0]*8)

    sale_table.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    elements.append(sale_table)
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    response.write(buff.getvalue())
    buff.close()
    return response

# @login_required()
# def edit_sale(request, pk):
#     tmp = get_name()
#     template = loader.get_template('sales/edit.html')
#     ins = get_object_or_404(Sale, pk=pk)
#     if request.method == 'POST':
#         form = SaleForm(request.POST, instance=ins)
#         if form.is_valid():
#             form.save()
#             message = 'Los datos se guardaron correctamente!'
#             tpl = loader.get_template('messages/message.html')
#             contextSuccess = {
#                 'title': get_body(tmp[3], tmp[0]),
#                 'uri': get_url('sales'),
#                 'message': message,
#             }
#             return HttpResponse(tpl.render(contextSuccess, request))
#     else:
#         form = SaleForm(instance=ins)
#     context = {
#         'title': get_body(tmp[3], tmp[0]),
#         'form': form,
#         'uri': get_url('sales'),
#     }
#     return HttpResponse(template.render(context, request))