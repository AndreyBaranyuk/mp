from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import AddProduct
from .models import Product
from django.urls import reverse
import datetime
from django.template import loader, Context

def index(request):
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render({"user": request.user}))


def add_product(request):
    if request.method == "POST":
        form = AddProduct(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
        else:
            print("FORM IS NOT VALID")
    else:
        form = AddProduct
    return render(request, 'product/add_product.html', {'form': form})
