from .models import Product
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'reason_dev', 'color', 'description', 'price', 'price', 'old_price',
                  'length', 'height', 'width')


