from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
import .models import ToolType
# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))


class InventoryListView(ListView):
    model = ToolType
    template_name = 'backend/inventory.html'
    context_object_name = tooltypes