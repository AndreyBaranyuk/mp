from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import AddProduct
from .models import Product
from django.views import generic
from django.template import loader, Context
from django.contrib.auth.models import User


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


class ProductD(generic.DetailView):
    template_name = 'product/product.html'
    model = Product


class Login(LoginView):
    redirect_to = '/'


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/accounts/login"
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.POST:
        if request.user.id != Product.objects.get(id=pk).seller:
            render(request, 'product/product_edited.html', {"message": "У вас нет прав на изменение этого товара"})
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.old_price = request.POST.get("old_price")
        product.color = request.POST.get("color")
        product.reason_dev = request.POST.get("reason_dev")
        product.width = request.POST.get("width")
        product.length = request.POST.get("length")
        product.height = request.POST.get("height")
        product.save()
        return HttpResponseRedirect(product.get_absolute_url())
    else:
        return render(request, 'product/edit_product.html', {"product": product})


def delete_product(request, pk):
    template_name = 'product/delete_product.html'
    msg = "Вы не продавец этого товара"
    if request.user == Product.objects.get(id=pk).seller:
        Product.objects.filter(id=pk).delete()
        msg = "Товар успешно удалён"
    return render(request, template_name, {"message": msg})


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
                seller = User.objects.all().get(username=request.POST['value'])
                queryset = Product.objects.all().filter(seller=seller.id)
            if param == "цвет":
                queryset = Product.objects.all().filter(color=request.POST['value'])
        return render(request, 'search/product_list.html', {'product_list': queryset})
