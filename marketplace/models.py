from django.db import models
from django.contrib.auth.models import User


# модель таблицы товаров в базе данных
class Product(models.Model):
    name = models.CharField(max_length=255)
    reason_dev = models.TextField(max_length=1023)
    color = models.CharField(max_length=50)
    description = models.TextField(max_length=1023)
    price = models.IntegerField()
    old_price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # ссылка на модель пользователя
    length = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    expose_datetime = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/product/%i" % self.id

    def __str__(self):
        return self.name

