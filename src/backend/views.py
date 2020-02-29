from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))

def inventory(request):
    template = loader.get_template("backend/inventory.html")
    return HttpResponse(template.render({}, request))