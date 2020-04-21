from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Customer


def index(request):
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render())


def login(request):
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render())


def login_form(request):
    return HttpResponse(template.render())
