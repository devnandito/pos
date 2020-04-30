from django import forms
from pos.levels.models import Level

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ('description',)