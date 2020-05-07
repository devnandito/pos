from django import forms
from pos.sales.models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('invoice', 'fkclient', 'fkuser', 'product', 'tax', 'net', 'total', 'payment',)

class CustomSaleForm(forms.ModelForm):
    seller = forms.CharField(max_length=140)
    sellerid = forms.IntegerField()
    class Meta:
        model = Sale
        fields = ('invoice', 'seller', 'fkclient', 'fkuser', 'product', 'tax', 'net', 'total', 'payment',)