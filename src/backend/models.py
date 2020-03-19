from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.

# Create your models here.
class ToolType(models.Model):
    type_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='default.jpeg', upload_to='tool_pics')
    slug = models.SlugField()
    def __str__(self):
        return f'{self.type_name}'

    def get_absolute_url(self):
        return reverse("product", kwargs={'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
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
    def __str__(self):
        return f'{self.quantity}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    is_reserved = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(null=True)
    checkout_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    checkin_date = models.DateTimeField(null=True)



