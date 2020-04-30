from django import forms
from pos.products.models import Product

MY_CHOICES = (
    ('10', '10%'),
    ('20', '20%'),
    ('30', '30%'),
    ('40', '40%'),
    ('50', '50%'),
    ('60', '60%'),
    ('70', '70%'),
    ('80', '80%'),
    ('90', '90%'),
    ('100', '100%'),
    )

class ProductForm(forms.ModelForm):
    sales_value = forms.ChoiceField(choices=MY_CHOICES)

    class Meta:
        model = Product
        fields = ('fkcategory', 'code', 'description', 'image', 'stock', 'purchase_price', 'sales_value',)