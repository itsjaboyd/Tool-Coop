from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import InventoryView, index, checkoutpage, ToolDetailView, add_to_cart,remove_single_tool_from_cart, remove_tool_from_cart, OrderSummaryView,add_tools, contact



urlpatterns = [
    path('', index, name='index'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('products/<slug>', ToolDetailView.as_view(), name='product'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', checkoutpage, name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-single-tool-from-cart/<slug>', remove_single_tool_from_cart, name='remove-single-tool-from-cart'),
    path('remove-tool-from-cart/<slug>', remove_tool_from_cart, name='remove-tool-from-cart'),
    path('add-tools/', add_tools, name='add-tools'),
	path('contact/', contact, name='contact'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)