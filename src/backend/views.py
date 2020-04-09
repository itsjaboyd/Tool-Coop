from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.views.generic import ListView,DetailView, View
from .models import ToolType, OrderItem, Order, Tool,Profile
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .forms import CheckoutForm,UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm, ProfileSelectForm,ToolTypeForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

# Create your views here.
def index(request):
    template = loader.get_template("backend/index.html")
    return HttpResponse(template.render({}, request))

def project(request):
    template = loader.get_template("backend/project-page.html")
    return HttpResponse(template.render({}, request))


def view_inventory(request):
    if request.method == 'POST':
        t_form = ToolTypeForm(request.POST or None, request.FILES)
        if t_form.is_valid():
            print("form is valid")
            print(settings.MEDIA_ROOT)
            print(t_form.cleaned_data['image'])
            tool_name = t_form.cleaned_data['type_name']
            quantity = t_form.cleaned_data['quantity']
            t_form.save()
            tool = ToolType.objects.get(type_name=tool_name)
            for x in range(quantity):
                Tool.objects.create(tool_type=tool,is_available=True)
            return redirect(request,"product", kwargs={'slug':tool.slug})
        else:
            print(form.errors.values)
            tools = ToolType.objects.all()
            context ={
                'tools':tools,
                't_form':t_form
            }
            messages.info(request, "Error:" + form.errors.values)
            return render(request, "backend/inventory-page.html", context)
    else:
        tools = ToolType.objects.all()
        t_form= ToolTypeForm()
        context ={
            'tools':tools,
            't_form':t_form
        }
        return render(request, "backend/inventory-page.html", context)


def view_product(request, slug):
    if request.method == 'POST':
        tool = ToolType.objects.get(slug=slug)
        t_form= ToolTypeForm(request.POST or None, request.FILES, instance=tool)
        if t_form.is_valid():
            t_form.save()
        context={
            'object': tool,
            't_form': t_form
        }
        return render(request,"backend/product-page.html", context)
    else:
        tool = ToolType.objects.get(slug=slug)
        t_form= ToolTypeForm(instance=tool,initial={ 'quantity': len(tool.tool_set.all()) })
        context={
            'object': tool,
            't_form': t_form
        }
        return render(request,"backend/product-page.html", context)
    

class AdminOrdersView(View):
    def get(self, *args, **kwargs):
        try:
            reserved_orders = Order.objects.filter(is_reserved=True, is_checked_out=False)
            checked_out_orders = Order.objects.filter(is_reserved=True, is_checked_out=True)
            overdue_orders = Order.objects.filter(due_date__lte=datetime.today() , is_checked_out=True)
            context=  {
                'reserved_orders': reserved_orders,
                'checked_out_orders': checked_out_orders,
                'overdue_orders': overdue_orders
            }
            return render(self.request, "backend/orders.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")

class OrderSummaryView(DetailView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_checked_out=False, is_reserved=False)
            p_form= ProfileSelectForm()
            context=  {
                'object': order,
                'p_form': p_form
            }
            return render(self.request, "backend/order-summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")
    def post(self, *args, **kwargs):
        form = ProfileSelectForm(self.request.POST or None)
        if form.is_valid():
            print('form is valid')
            user_id = form.cleaned_data['customer_id']
            print(user_id)
            order = Order.objects.get(user=self.request.user, is_reserved=False, is_checked_out=False)
            order.user = User.objects.get(id=user_id)
            order.save()
            return redirect("/admin-order-summary/" + str( order.id))

class AdminOrderSummaryView(DetailView):
    def get(self, *args, **kwargs):
        try:
            print(kwargs['id'])
            order = Order.objects.get(pk=kwargs['id'])
            o_form = CheckoutForm()
            p_form = ProfileUpdateForm()
            o_form.instance.start_date = datetime.today
            context=  {
                'object': order,
                'o_form': o_form
            }
            return render(self.request, "backend/admin-order-summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('form is valid')
            print(kwargs)
            order = Order.objects.get(pk=kwargs['id'])
            order.reservation_date = datetime.today()
            order.checkout_date = datetime.today()
            order.due_date = form.cleaned_data['end_date']
            order.is_reserved = True
            order.is_checked_out =True
            for item in order.items.all():
                item.is_reserved = True
                item.is_checked_out = True
                for x in range(item.quantity):
                    tool_item = Tool.objects.filter(tool_type = item.tool, is_available=True)[0]
                    tool_item.is_available = False
                    tool_item.save()
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
        if(self.request.user.is_superuser):
            return redirect('admin-order-summary/'+ str(order.id))
        profile = Profile.objects.get(user=self.request.user)
        if(profile.city == ''):
            messages.info(self.request, f'You must update your profile information before you can checkout.')
            return redirect('edit-profile')
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
            order.reservation_date = datetime.now()
            order.checkout_date = form.cleaned_data['start_date']
            order.due_date = form.cleaned_data['end_date']
            order.is_reserved = True
            for item in order.items.all():
                item.is_reserved = True
                item.is_checked_out = False
                for x in range(item.quantity):
                    tool_item = Tool.objects.filter(tool_type = item.tool, is_available=True)[0]
                    tool_item.is_available = False
                    tool_item.save()
                item.save()
            order.save()
            messages.info(self.request, "Reservation Sent!")
            return redirect('index')
        else:
            messages.info(self.request, "Error: Checkout could not be completed!")
            return redirect('checkout')




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

def checkin_tools(request, id):
    order = Order.objects.get(pk=id)
    order.checkin_date =  datetime.today()
    for item in order.items.all():
        for x in range(item.quantity):
            tool_item = Tool.objects.filter(tool_type=item.tool, is_available=False).first()
            tool_item.is_available = True
            tool_item.save()
        item.is_checked_out = False
        item.is_reserved = False
        item.save()
        order.is_reserved = False
        order.is_checked_out = False
        order.save()
    messages.info(request, "Order Checked In")
    return redirect("orders")

def add_to_cart(request, slug):
    tool_type= get_object_or_404(ToolType, slug=slug)
    if len(tool_type.get_available()) > 0:
        order_qs = Order.objects.filter(user= request.user, is_checked_out=False, is_reserved=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(tool_id=tool_type.id).exists():
                order_item = order.items.get(tool_id=tool_type.id)
                if order_item.quantity == tool_type.get_available():
                    messages.info(request, "You cannot add more of this tool.")
                    return redirect("order-summary")
                else:
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

def get_remove_tool_from_inventory(self):
        return reverse()
def get_remove_single_tool_from_inventory(self):
    return reverse()
def get_add_tool_from_inventory(self):
    tool = Tool.objects.create(tool_type=self, is_available=True)
    return reverse()

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


def setup(request):
    User.objects.create_superuser(username='Joe', password='joespassword', email='')
    User.objects.create_superuser(username='admin', password='123', email='')
    add_tool_helper("Axe", 'axe', 3)
    add_tool_helper("Chisel", 'chisel', 4)
    add_tool_helper("Circular Saw", 'circular-saw', 1)
    add_tool_helper("Crowbar", 'crowbar', 5)
    add_tool_helper("Drill", 'drill', 2)
    add_tool_helper("File", 'file', 5)
    add_tool_helper("Hammer", 'hammer', 5)
    add_tool_helper("Hand Saw", 'hand-saw', 1)
    add_tool_helper("Hex Keys", 'hex-keys', 4)
    add_tool_helper("Jigsaw", 'jigsaw', 1)
    add_tool_helper("Level", 'level', 5)
    add_tool_helper("Mallet", 'mallet', 2)
    add_tool_helper("Pliers", 'pliers', 5)
    add_tool_helper("Rotary Tool", 'rotary-tool', 1)
    add_tool_helper("Screwdriver", 'screwdriver', 5)
    add_tool_helper("Sledgehammer", 'sledgehammer', 3)
    add_tool_helper("Soldering Iron", 'soldering-iron', 1)
    add_tool_helper("Square", 'square', 2)
    add_tool_helper("Tape Measure", 'tape-measure', 5)
    add_tool_helper("Wire Cutters", 'wire-cutters', 3)
    return redirect('index')
	

def add_tool_helper(tool_name, tool_slug, quantity):
    f= open("..\\tools\\"+ tool_slug+".txt","r")
    description =f.read()
    ToolType.objects.create(type_name=tool_name, description=description, slug='axe', image='tool_pics/'+tool_slug+'.jpg')
    tool = get_object_or_404(ToolType, type_name=tool_name)
    for x in range (quantity):
        Tool.objects.create(tool_type=tool)