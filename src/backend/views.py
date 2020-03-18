from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
from .models import ToolType
# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))

def productpage(request):
    template = loader.get_template("backend/product-page.html")
    return HttpResponse(template.render({}, request))

def checkoutpage(request):
    template = loader.get_template("backend/checkout-page.html")
    return HttpResponse(template.render({}, request))


def inventory_list(request):
    context = {
        'items': ToolType.objects.all()
    }
    return render(request, "backend/inventory-page.html", context)