from django import forms
from .models import Product


# class AddProduct(forms.Form):
#     name = forms.CharField(max_length=255)
#     reason_dev = forms.CharField(max_length=1023)
#     color = forms.CharField(max_length=50)
#     description = forms.CharField(max_length=1023)
#     price = forms.IntegerField()
#     old_price = forms.IntegerField()
#     length = forms.IntegerField()
#     height = forms.IntegerField()
#     width = forms.IntegerField()

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'reason_dev', 'color', 'description', 'price', 'price', 'old_price',
                  'length', 'height', 'width')


