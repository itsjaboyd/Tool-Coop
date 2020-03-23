from django.contrib import admin
from .models import ToolType, Tool, Order, OrderItem, Profile
# Register your models here.

admin.site.register(ToolType)
admin.site.register(Tool)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Profile)