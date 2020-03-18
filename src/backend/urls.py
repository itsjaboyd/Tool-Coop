from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import InventoryView, index, checkoutpage, ToolDetailView



urlpatterns = [
    path('', index, name='index'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('products/<slug>', ToolDetailView.as_view(), name='product'),
    path('checkout/', checkoutpage, name='checkout'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)