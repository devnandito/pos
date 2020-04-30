from django import forms
from pos.categories.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('description',)