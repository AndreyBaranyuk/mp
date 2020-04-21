from django.contrib import admin
from .models import Ad
from .models import Product
from .models import Seller
from .models import Customer
from .models import Category
from .models import Subcategory
from .models import Image


admin.site.register(Ad)
admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Image)

