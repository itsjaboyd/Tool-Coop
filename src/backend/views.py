from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
from .models import ToolType, Tool
# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))


class InventoryListView(ListView):
    model = ToolType
    template_name = 'backend/inventory.html'
    context_object_name = 'tooltypes'


def product(request, tool_id):
    # find the tool through the tool_id
    tool = Tool.objects.get(pk=tool_id)
    toolType = tool.tool_type

    context = {
        'tool': tool,
        'tool_type': toolType,
    }

    return render(request, 'backend/product.html', context)

