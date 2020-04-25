from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import inspect
from .forms import AddProduct
from .models import Product
from django.views import generic
from django.template import loader, Context


def index(request):
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render({"user": request.user}))


def add_product(request):
    if request.method == "POST":
        form = AddProduct(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
        else:
            print("FORM IS NOT VALID")
    else:
        form = AddProduct
    return render(request, 'product/add_product.html', {'form': form})


def explanation(request):
    import os
    cmd = "notepad.exe explanation/explanation.txt"
    os.system(cmd)
    print(os.curdir)
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render({"user": request.user}))


class ProductList(generic.ListView):
    model = Product
    context_object_name = 'product_list'
    queryset = Product.objects
    template_name = 'search/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Product.objects.all()


def product_list_sort(request):
    if request.method == "POST":
        param = request.POST['param']
        queryset = Product.objects.all()
        if request.POST['name'] == 'sort':
            if param == "дешевле":
                queryset = sorted(queryset, key=lambda k: k.price, reverse=False)
                return render(request, 'search/product_list.html', {'product_list': queryset})
            if param == "дороже":
                queryset = sorted(queryset, key=lambda k: k.price, reverse=True)
                return render(request, 'search/product_list.html', {'product_list': queryset})
            if param == "минимальная цена":
                mini = []
                queryset = sorted(queryset, key=lambda k: k.price, reverse=False)
                mini.append(queryset[0])
                return render(request, 'search/product_list.html', {'product_list': mini})
            if param == "максимальная цена":
                maxi = []
                queryset = sorted(queryset, key=lambda k: k.price, reverse=True)
                maxi.append(queryset[0])
                return render(request, 'search/product_list.html', {'product_list': maxi})
            if param == "средняя цена":
                sum = 0
                for i in queryset:
                    sum += i.price
                mid_price = sum/queryset.count()
                return render(request, 'search/product_list.html', {'mid_price': mid_price})
            if param == "сначала новые":
                queryset = sorted(queryset, key=lambda k: k.expose_datetime, reverse=True)
                return render(request, 'search/product_list.html', {'product_list': queryset})
            if param == "сначала старые":
                queryset = sorted(queryset, key=lambda k: k.expose_datetime)
                return render(request, 'search/product_list.html', {'product_list': queryset})
            params = []
            for i in Product.objects.all():
                if param == "продавец":
                    params.append(i.seller)
                if param == "цвет":
                    params.append(i.color)
            return render(request, 'search/product_list.html', {'product_list': queryset,
                                                                'second': True,
                                                                'param': param,
                                                                'params': params})
        if request.POST['name'] == 'sort_param':
            if param == "продавец":
                queryset = Product.objects.all().filter(seller=request.POST['value'])
            if param == "цвет":
                queryset = Product.objects.all().filter(color=request.POST['value'])
        return render(request, 'search/product_list.html', {'product_list': queryset})
