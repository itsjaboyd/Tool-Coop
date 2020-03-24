from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
# Create your models here.

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    phone = PhoneNumberField(blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pic')

    def __str__(self):
        return f'{self.user.username} Profile'
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            size = (300,300)
            img.thumbnail(size)
            img.save(self.image.path)


class ToolType(models.Model):
    type_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='default.jpeg', upload_to='tool_pics')
    slug = models.SlugField(unique=True)
    def __str__(self):
        return f'{self.type_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type_name)
        super(ToolType, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("product", kwargs={'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_tool_from_cart(self):
        return reverse("remove-tool-from-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_single_from_cart_url(self):
        return reverse("remove-single-tool-from-cart", kwargs={
            'slug': self.slug
        })
    
    def get_available(self):
        return self.tool_set.all().filter(is_available=True)


class Tool(models.Model):
    tool_type = models.ForeignKey(ToolType, on_delete=models.CASCADE)
    is_available = models.BooleanField (default=True)

    def __str__(self):
        return f'{self.tool_type.type_name}'


class OrderItem(models.Model):
    tool = models.ForeignKey(ToolType,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_reserved = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.tool.type_name} - {self.quantity}'
    
    def reserve_tool(self):
        self.is_reserved = True
        for x in range(self.quantity):
            tool_item = Tool.objects.filter(tool_type = self.tool, is_available=True)[0]
            tool_item.is_reserved = True

    def checkout_tool(self):
        self.is_reserved = True
        self.is_checked_out = True
        for x in range(self.quantity):
            tool_item = Tool.objects.filter(tool_type = self.tool, is_available=True)[0]
            tool_item.is_reserved = True
    
    def checkin_tool(self):
        self.is_reserved = False
        for x in range(self.quantity):
            tool_item = Tool.objects.filter(tool_type = self.tool, is_available=False)[0]
            tool_item.is_reserved = False
            


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    is_reserved = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(null=True)
    checkout_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    checkin_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.user.username} - {self.checkout_date}'
    
    def get_item_total(self):
        item_count = 0
        for item in self.items.all():
            item_count += item.quantity
        return item_count
    
    def reserve_order_items(self):
        for item in items.all():
            item.reserve_tool()
    def checkout_order_items(self):
        for item in items.all():
            item.checkout_tool()
    def checkin_order_item(self):
        for item in items.all():
            item.checkin_tool()

    def get_absolute_url(self):
        return reverse("previous-order-summary", kwargs={'id':self.id})
    def get_admin_order_summary(self):
        return reverse("admin-order-summary", kwargs={'id':self.id})