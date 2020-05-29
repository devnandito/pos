from django import forms
from pos.sales.models import Sale
from pos.clients.models import Client

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('invoice', 'fkclient', 'fkuser', 'product', 'tax', 'net', 'total', 'payment',)

MY_CLIENTS = [(choice.pk, choice) for choice in Client.objects.all()]
MY_PAY = (
    ('', 'Metodo de pago'),
    ('efectivo', 'Efectivo'),
    ('TD', 'Debito'),
    ('TC', 'Credito'),
    )

class CustomSaleForm(forms.Form):
    invoice = forms.IntegerField()
    seller = forms.CharField(max_length=140)
    sellerid = forms.IntegerField()
    new_tax_sale = forms.IntegerField(
        error_messages={'required': 'Ingrese impuesto'}, 
        widget=forms.TextInput(
            attrs={'required': True, 'min': '1', 'placeholder': '0', 'type': 'number'}
        )
    )
    new_total_sale = forms.CharField(
        widget=forms.TextInput(
            attrs={'total': '', 'required': True, 'min': '1', 'placeholder': '0', 'readonly': True}
        )
    )
    new_method_pay = forms.ChoiceField(choices=MY_PAY)
    fkclient = forms.ChoiceField(choices=[('', '---Seleccionar cliente---')] + MY_CLIENTS)

class CustomEditSaleForm(forms.Form):
    invoice = forms.IntegerField()
    seller = forms.CharField(max_length=140)
    sellerid = forms.IntegerField()
    new_tax_sale = forms.IntegerField(
        error_messages = {'required': 'Ingrese impuesto'}, 
        widget = forms.TextInput(
            attrs = {'required': True, 'min': '1', 'placeholder': '0', 'type': 'number'}
        )
    )
    new_total_sale = forms.CharField(
        widget = forms.TextInput(
            attrs = {'total': '', 'required': True, 'min': '1', 'placeholder': '0', 'readonly': True}
        )
    )
    new_method_pay = forms.ChoiceField(choices=MY_PAY)
    fkclient = forms.CharField(
        widget = forms.TextInput(
            attrs = {'readonly': True, 'hidden': True}
        )
    )
    nameclient = forms.CharField(
        widget = forms.TextInput(
            attrs = {'readonly': True}
        )
    )

# class CustomEditSaleForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     self.fkclient = kwargs.pop('fkclient')
    #     super(CustomEditSaleForm, self).__init__(*args, **kwargs)
    #     self.fields['fkclient'].initial = self.fkclient
    #     self.fields['fkclient'].initial = Client.objects.filter(pk=self.fkclient)
    #     self.fields['fkclient'].widget = CheckboxInput(required=False)

    # invoice = forms.IntegerField()
    # seller = forms.CharField(max_length=140)
    # sellerid = forms.IntegerField()
    # new_tax_sale = forms.IntegerField(
    #     error_messages = {'required': 'Ingrese impuesto'}, 
    #     widget = forms.TextInput(
    #         attrs = {'required': True, 'min': '1', 'placeholder': '0', 'type': 'number'}
    #     )
    # )
    # new_total_sale = forms.CharField(
    #     widget = forms.TextInput(
    #         attrs = {'total': '', 'required': True, 'min': '1', 'placeholder': '0', 'readonly': True}
    #     )
    # )
    # new_method_pay = forms.ChoiceField(choices=MY_PAY)
    # fkclient = forms.CharField(
    #     widget = forms.TextInput(
    #         attrs = {'readonly': True, 'hidden': True}
    #     )
    # )
    # nameclient = forms.CharField(
    #     widget = forms.TextInput(
    #         attrs = {'readonly': True}
    #     )
    # )