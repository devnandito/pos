from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from pos.users.models import User, Profile

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','username', 'first_name', 'last_name', 'password1', 'password2', )

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active')

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('level', 'description', 'picture',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'level', 'description', 'picture',)

# class CustomEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('user', 'username', 'first_name', 'last_name',)
#         exclude = ('password1', 'password2',)