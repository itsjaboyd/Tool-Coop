from django.contrib import admin
from .models import ToolType, Tool, ReservationLog, ReservationLogTools
# Register your models here.

admin.site.register(ToolType)
admin.site.register(Tool)
admin.site.register(ReservationLog)
admin.site.register(ReservationLogTools)