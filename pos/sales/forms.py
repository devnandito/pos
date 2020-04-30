from django import forms
from pos.sales.models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('code', 'fkclient', 'fkuser', 'product', 'tax', 'net', 'total', 'payment',)