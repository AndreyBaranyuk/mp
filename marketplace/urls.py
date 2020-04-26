from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list', views.ProductList.as_view(), name='product_list'),
    path('product_list_sort/', views.product_list_sort, name='product_list_sort'),
    path('explanation', views.explanation, name='explanation'),
    url(r'^product/(?P<pk>\d+)/edit', views.edit_product, name='edit_product'),
    url(r'^product/(?P<pk>\d+)/delete', views.delete_product, name='product_delete'),
    url(r'^product/(?P<pk>\d+)/', views.ProductD.as_view(), name='product')
]
