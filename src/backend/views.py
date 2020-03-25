from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.views.generic import ListView,DetailView, View
from .models import ToolType, OrderItem, Order, Tool,Profile
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .forms import CheckoutForm,UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))

def project(request):
    template = loader.get_template("backend/project-page.html")
    return HttpResponse(template.render({}, request))


class InventoryView(ListView):
    model = ToolType
    template_name = "backend/inventory-page.html"

class ToolDetailView(DetailView):
    model = ToolType
    template_name = "backend/product-page.html"

class AdminOrdersView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter( is_checked_out=False, is_reserved=True)
            context=  {
                'object_list': order
            }
            return render(self.request, "backend/orders.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")

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

class AdminOrderSummaryView(DetailView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['id'])
            context=  {
                'object': order,
            }
            return render(self.request, "backend/admin-order-summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('form is valid')
            print(str(form['start_date'].value))
            order = Order.objects.get(user=self.request.user, is_reserved=False, is_checked_out=False)
            if order.reservation_date == null:
                order.reservation_date = datetime.today()
            order.checkout_date = datetime.today()
            order.due_date = form.cleaned_data['end_date']
            order.is_reserved = True
            for item in order.items.all():
                item.is_reserved = True
                item.is_checked_out = True
                for x in range(item.quanity):
                    tool_item = Tool.objects.filter(tool_type = item.tool, is_available=True)[0]
                    tool_item.is_reserved = True
                    tool_item.is_checked_out=True
            order.save()
            messages.info(self.request, "Checkout Completed!")
            return redirect('index')


class PreviousOrderSummaryView(DetailView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, pk=kwargs['id'])
            context=  {
                'object': order
            }
            return render(self.request, "backend/previous-order-summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Order Not Found")
            return redirect("profile")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_reserved=False, is_checked_out=False)
        profile = Profile.objects.get(user=self.request.user)
        o_form = CheckoutForm()
        context= {
            'o_form': o_form,
            'order': order,
            'profile': profile
        }
        return render(self.request, "backend/checkout-page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('form is valid')
            print(str(form['start_date'].value))
            order = Order.objects.get(user=self.request.user, is_reserved=False, is_checked_out=False)
            order.reservation_date = form.cleaned_data['start_date']
            order.due_date = form.cleaned_data['end_date']
            order.is_reserved = True
            for item in order.items.all():
                item.is_reserved = True
                item.is_checked_out = False
                for x in range(item.quantity):
                    tool_item = Tool.objects.filter(tool_type = item.tool, is_available=True)[0]
                    tool_item.is_reserved = True
                    tool_item.is_checked_out=False
            order.save()
            messages.info(self.request, "Reservation Sent!")
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
    orders = Order.objects.filter(user=request.user)
    context = {
        'profile' : profile,
        'orders' : orders,
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
            messages.info(request, "Your Message Was sent")
            return redirect('contact')

    return render(request, 'contact', {
        'form': form_class,
    })


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
    for x in range (10):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="File")
    for x in range (20):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Hand Saw")
    for x in range (15):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Hex Keys")
    for x in range (10):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Jigsaw")
    for x in range (5):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Level")
    for x in range (20):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Mallet")
    for x in range (10):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Pliers")
    for x in range (20):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Rotary Tool")
    for x in range (5):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Screwdriver")
    for x in range (50):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Sledgehammer")
    for x in range (5):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Soldering Iron")
    for x in range (8):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Square")
    for x in range (10):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Tape Measure")
    for x in range (15):
        Tool.objects.create(tool_type=tool)
    tool = get_object_or_404(ToolType, type_name="Wire Cutters")
    for x in range (20):
        Tool.objects.create(tool_type=tool)
    return redirect('index')
	

