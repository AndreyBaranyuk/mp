from django.db import models
from django.contrib.auth.models import User

# class Category(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


# class Subcategory(models.Model):
#     name = models.CharField(max_length=50)
#     category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    reason_dev = models.TextField(max_length=1023)
    color = models.CharField(max_length=50)
    description = models.TextField(max_length=1023)
    price = models.IntegerField()
    old_price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    # seller = models.CharField(max_length=255)
    # category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    # subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    length = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    expose_datetime = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/product/%i" % self.id

    def __str__(self):
        return self.name

