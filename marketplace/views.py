from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import AddProduct, RegistrationForm
from .models import Product
from django.views import generic
from django.template import loader, Context
from django.contrib.auth.models import User, Group

# главная страница
def index(request):
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render({"user": request.user}))


# страница добавления продукта
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


# вызов справки
def explanation(request):
    import os
    cmd = "notepad.exe explanation/explanation.txt"  # с помощью вызоыва блокнота через командную строку
    os.system(cmd)
    print(os.curdir)
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render({"user": request.user}))


# список продуктов
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


# подробное представление продукта
class ProductD(generic.DetailView):
    template_name = 'product/product.html'
    model = Product


# авторизация
class Login(LoginView):
    redirect_to = '/'


# регистрация
def register(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.username = form.cleaned_data['username']
        new_user.set_password(form.cleaned_data['password1'])
        new_user.email = form.cleaned_data['email']
        new_user.save()
        new_user.groups.add(Group.objects.get(name='customer'))
        return HttpResponseRedirect('/accounts/login')
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


# редактирование продукта
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


# удаление продукта
def delete_product(request, pk):
    template_name = 'product/delete_product.html'
    msg = "Вы не продавец этого товара"
    if request.user == Product.objects.get(id=pk).seller:
        Product.objects.filter(id=pk).delete()
        msg = "Товар успешно удалён"
    return render(request, template_name, {"message": msg})


# сортировка продуктов по различным признакам
def product_list_sort(request):
    queryset = Product.objects.all()
    if request.method == "POST":
        param = request.POST['param']  # признак сортировки
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
            params = []  # список для отображению пользователей продавцов или цветов на выбор
            for i in Product.objects.all():
                if param == "продавец":
                    params.append(i.seller)
                if param == "цвет":
                    params.append(i.color)
            params = list(set(params))
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
    return render(request, 'search/product_list.html', {'product_list': queryset})
