from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView
from .models import ToolType, OrderItem, Order
# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))


def checkoutpage(request):
    template = loader.get_template("backend/checkout-page.html")
    return HttpResponse(template.render({}, request))

class InventoryView(ListView):
    model = ToolType
    template_name = "backend/inventory-page.html"

class ToolDetailView(DetailView):
    model = ToolType
    template_name = "backend/product-page.html"

def add_to_cart(request, slug):
    tool_type= get_object_or_404(ToolType.slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_)