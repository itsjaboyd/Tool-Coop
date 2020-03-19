from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.views.generic import ListView,DetailView
from .models import ToolType, OrderItem, Order
from django.utils import timezone
from django.contrib import messages

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

class OrderSummaryView(DetailView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_checked_out=False, is_reserved=False)
            context=  {
                'object': order
            }
            return render(self.request, "backend/order-summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")
        

def add_to_cart(request, slug):
    tool_type= get_object_or_404(ToolType, slug=slug)
    order_item = OrderItem.objects.create(tool=tool_type)
    order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(tool_id=tool_type.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quanity updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("order-summary")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    

def remove_tool_from_cart(request, slug):
    tool_type= get_object_or_404(ToolType, slug=slug)
    order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(tool_id=tool_type.id).exists():
            order_item = OrderItem.objects.filter(tool=tool_type, user = request.user, is_checked_out=False, is_reserved=False)
            order.items.remove(order_item[0])
            order_item.delete()
            messages.info(request, "This tool was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This tool was not in your cart.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)
    


def remove_single_tool_from_cart(request, slug):
    tool_type= get_object_or_404(ToolType, slug=slug)
    order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(tool_id=tool_type.id).exists():
            order_item = OrderItem.objects.filter(tool=tool_type, user = request.user, is_checked_out=False, is_reserved=False)
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, "This tool quantity updated.")
                return redirect("order-summary")
            else:
                order.items.remove(order_item[0])
                order_item.delete()
                messages.info(request, "This tool was removed from your cart.")
                return redirect("order-summary")
        else:
            messages.info(request, "This tool was not in your cart.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)

