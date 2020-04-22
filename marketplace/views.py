from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


def index(request):
    template = loader.get_template('landing/index.html')
    return HttpResponse(template.render({"user": request.user}))
