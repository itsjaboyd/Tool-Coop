from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.views.generic import ListView,DetailView
from .models import ToolType, OrderItem, Order, Tool
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .forms import ContactForm

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
    if len(tool_type.get_available()) > 0:
        order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(tool_id=tool_type.id).exists():
                order_item = order.items.get(tool_id=tool_type.id)
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quanity updated.")
                return redirect("order-summary")
            else:
                order_item = OrderItem.objects.create(tool=tool_type)
                messages.info(request, "This item was added to your cart.")
                order.items.add(order_item)
                return redirect("order-summary")
        else:
            order_item = OrderItem.objects.create(tool=tool_type)
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        messages.info(request, "This tool is currently unavailable.")
        return redirect("order-summary")
    

def remove_tool_from_cart(request, slug):
    tool_type= get_object_or_404(ToolType, slug=slug)
    order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(tool_id=tool_type.id).exists():
            order_item = order.items.filter(tool=tool_type)
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
            order_item = order.items.get(tool=tool_type)
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, "This tool quantity updated.")
                return redirect("order-summary")
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This tool was removed from your cart.")
                return redirect("order-summary")
        else:
            messages.info(request, "This tool was not in your cart.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product", slug=slug)


def add_tools(request):
    tool = get_object_or_404(ToolType, type_name="Axe")
    for x in range (3):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Chisel")
    for x in range (7):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Drill")
    for x in range (5):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Crowbar")
    for x in range (10):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Circular Saw")
    for x in range (3):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Hammer")
    for x in range (15):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="File")
    for x in range (20):
        Tool.objects.create(tool_type=tool)
    return redirect('index')
	
def contact(request):
    template = loader.get_template("backend/contact.html")
    return HttpResponse(template.render({}, request))

    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_first_name = request.POST.get(
                'contact_first_name'
            , '')
            contact_last_name = request.POST.get(
                'contact_last_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('Email_template.txt')
            context = {
                'contact_first_name': contact_first_name,
				'contact_last_name': contact_last_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact', {
        'form': form_class,
    })