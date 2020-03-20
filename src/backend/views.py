from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.views.generic import ListView,DetailView, View
from .models import ToolType, OrderItem, Order, Tool,Profile
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm,UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
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

class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_reserved=False, is_checked_out=False)
        o_form = CheckoutForm(instance=order)
        p_form = ProfileUpdateForm(instance=order.user.profile)
        u_form = UserUpdateForm(instance=self.request.user)

        context= {
            'o_form': o_form,
            'p_form': p_form,
            'u_form': u_form,
            'order': order
        }
        return render(self.request, "backend/checkout-page.html", context)    

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            messages.info(request, "Reservation Sent!")
            return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form= UserRegisterForm()
    return render(request, 'backend/register.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile' : profile,
    }
    return render(request, 'backend/profile.html',context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'backend/profile-edit.html',context)
         

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