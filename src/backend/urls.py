from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import InventoryView, index, checkoutpage, ToolDetailView, add_to_cart



urlpatterns = [
    path('', index, name='index'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('products/<slug>', ToolDetailView.as_view(), name='product'),
    path('checkout/', checkoutpage, name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)